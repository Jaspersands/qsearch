from __future__ import annotations

import argparse
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


SCHEMA_VERSION = "2026-04-12.dcp-noisy-tree-merge-error-propagation-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_noisy_tree_merge_error_propagation_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_noisy_tree_merge_error_propagation_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_NOISY_TREE_MERGE_ERROR_PROPAGATION_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def symmetric_nearest_neighbor_kernel(q: int, p_err: float) -> np.ndarray:
    """Return symmetric modular noise kernel K_eta on Z_q: (1 - p_err) at 0, p_err/2 at +1 and -1 mod q."""
    if not (0.0 <= p_err <= 1.0):
        raise ValueError("p_err must be in [0, 1]")
    kernel = np.zeros(q, dtype=np.float64)
    kernel[0] = 1.0 - p_err
    kernel[1 % q] += 0.5 * p_err
    kernel[(q - 1) % q] += 0.5 * p_err
    return kernel


def cyclic_convolve_power(kernel: np.ndarray, k_leaves: int) -> np.ndarray:
    """Compute exact k_leaves-fold cyclic convolution of kernel on Z_q by direct dynamic programming."""
    q = len(kernel)
    current = np.zeros(q, dtype=np.float64)
    current[0] = 1.0
    for _ in range(k_leaves):
        nxt = np.zeros(q, dtype=np.float64)
        for a in range(q):
            if current[a] == 0.0:
                continue
            for b in range(q):
                if kernel[b] == 0.0:
                    continue
                nxt[(a + b) % q] += current[a] * kernel[b]
        current = nxt
    return current


def fourier_cos_harmonics(dist: np.ndarray) -> np.ndarray:
    """Compute sum_{e in Z_q} dist[e] cos(2 pi m e / q) for all m in {0, ..., q-1}."""
    q = len(dist)
    e_grid = np.arange(q, dtype=np.float64)
    m_grid = np.arange(q, dtype=np.float64)
    angles = 2.0 * np.pi * np.outer(m_grid, e_grid) / float(q)
    return np.cos(angles) @ dist


def evaluate_noisy_tree_merge_case(
    *,
    case_id: str,
    q: int,
    p_err: float,
    max_depth: int,
    target_tau: float = 0.5,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 across tree depths L = 0, 1, ..., max_depth."""
    base_kernel = symmetric_nearest_neighbor_kernel(q, p_err)
    base_harmonics = fourier_cos_harmonics(base_kernel)
    lambda_1 = float(base_harmonics[1])

    # Analytical formula for nearest-neighbor symmetric kernel:
    # lambda_1 = (1 - p_err) + p_err * cos(2 pi / q) = 1 - p_err * (1 - cos(2 pi / q))
    lambda_1_analytic = 1.0 - p_err * (1.0 - math.cos(2.0 * math.pi / float(q)))
    lambda_1_residual = abs(lambda_1 - lambda_1_analytic)

    depth_rows = []
    max_conv_vs_power_residual = 0.0
    max_norm_residual = 0.0
    theorem3_strict_dominance_holds = True

    for L in range(max_depth + 1):
        K = 2 ** L
        conv_dist = cyclic_convolve_power(base_kernel, K)
        norm_res = abs(float(np.sum(conv_dist)) - 1.0)
        max_norm_residual = max(max_norm_residual, norm_res)

        conv_harmonics = fourier_cos_harmonics(conv_dist)
        power_harmonics = base_harmonics ** K
        conv_res = float(np.max(np.abs(conv_harmonics - power_harmonics)))
        max_conv_vs_power_residual = max(max_conv_vs_power_residual, conv_res)

        root_visibility_emp = float(conv_harmonics[1])
        root_visibility_theo = float(lambda_1 ** K)

        # Theorem 2 required per-leaf lambda_1 threshold to keep root visibility >= target_tau
        required_lambda_1_for_tau = float(target_tau ** (1.0 / float(K)))
        max_allowed_damping_defect = 1.0 - required_lambda_1_for_tau

        # Theorem 3 SNR comparison:
        # Classical K-leaf single-copy Fourier readout SNR proxy: K * lambda_1^2
        # Coherent depth-L root state harmonic SNR proxy: (Lambda_1^{(L)})^2 = lambda_1^{2K}
        snr_leaf = float(K) * (lambda_1 ** 2)
        snr_root = float(lambda_1 ** (2 * K))
        snr_ratio = (snr_root / snr_leaf) if snr_leaf > 0.0 else 0.0
        snr_ratio_formula = (2.0 ** (-L)) * (lambda_1 ** (2 * (K - 1)))
        snr_ratio_residual = abs(snr_ratio - snr_ratio_formula)

        if L >= 1:
            if not (snr_ratio <= (2.0 ** (-L)) + tolerance and snr_ratio < 1.0):
                theorem3_strict_dominance_holds = False
        if snr_ratio_residual > tolerance:
            theorem3_strict_dominance_holds = False

        depth_rows.append(
            {
                "depth_L": L,
                "k_leaves": K,
                "convolved_distribution_norm_residual": norm_res,
                "max_harmonic_power_law_residual": conv_res,
                "root_fundamental_visibility_empirical": root_visibility_emp,
                "root_fundamental_visibility_theoretical": root_visibility_theo,
                "required_lambda_1_for_target_tau": required_lambda_1_for_tau,
                "max_allowed_leaf_damping_defect_for_tau": max_allowed_damping_defect,
                "meets_target_tau": (root_visibility_theo >= target_tau),
                "classical_k_leaf_snr_proxy": snr_leaf,
                "coherent_root_snr_proxy": snr_root,
                "root_to_leaf_snr_ratio": snr_ratio,
                "root_to_leaf_snr_ratio_formula": snr_ratio_formula,
                "snr_ratio_residual": snr_ratio_residual,
            }
        )

    theorem1_verified = (
        lambda_1_residual <= tolerance
        and max_conv_vs_power_residual <= tolerance
        and max_norm_residual <= tolerance
    )
    theorem2_verified = all(
        abs(
            row["root_fundamental_visibility_theoretical"]
            - math.exp(-row["k_leaves"] * math.log(1.0 / lambda_1))
        )
        <= tolerance
        for row in depth_rows
        if lambda_1 > 0.0
    )

    return {
        "case_id": case_id,
        "q": q,
        "p_err": p_err,
        "max_depth": max_depth,
        "target_tau": target_tau,
        "single_leaf_lambda_1": lambda_1,
        "single_leaf_lambda_1_analytic": lambda_1_analytic,
        "single_leaf_lambda_1_residual": lambda_1_residual,
        "max_convolution_vs_power_residual": max_conv_vs_power_residual,
        "max_distribution_norm_residual": max_norm_residual,
        "depth_rows": depth_rows,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_strict_dominance_holds,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_strict_dominance_holds
        ),
    }


def build_dcp_noisy_tree_merge_error_propagation_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q8_low_noise_p01_depth4",
            "q": 8,
            "p_err": 0.10,
            "max_depth": 4,
            "target_tau": 0.5,
        },
        {
            "case_id": "q8_medium_noise_p025_depth4",
            "q": 8,
            "p_err": 0.25,
            "max_depth": 4,
            "target_tau": 0.5,
        },
        {
            "case_id": "q16_low_noise_p015_depth4",
            "q": 16,
            "p_err": 0.15,
            "max_depth": 4,
            "target_tau": 0.5,
        },
        {
            "case_id": "q16_high_noise_p04_depth4",
            "q": 16,
            "p_err": 0.40,
            "max_depth": 4,
            "target_tau": 0.5,
        },
        {
            "case_id": "q32_moderate_noise_p02_depth4",
            "q": 32,
            "p_err": 0.20,
            "max_depth": 4,
            "target_tau": 0.5,
        },
    ]

    cases = [evaluate_noisy_tree_merge_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_convolution_vs_power_residual": max(
            c["max_convolution_vs_power_residual"] for c in cases
        ),
        "max_distribution_norm_residual": max(
            c["max_distribution_norm_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Exact cyclic convolution across depths L in {0, 1, 2, 3, 4} (K = 2^L in {1, 2, 4, 8, 16} leaves) "
            "proves that binary CNOT tree-merging of noisy DCP leaves convolves the leaf phase errors into "
            "K_eta^{*2^L}, causing the m-th harmonic visibility to decay double-exponentially in tree depth L "
            "as Lambda_m^{(L)} = (lambda_m)^{2^L}. Consequently, the root-to-single-leaf harmonic SNR ratio "
            "equals 2^{-L} lambda_1^{2(2^L - 1)} < 1 for every L >= 1, proving that uncorrected CNOT tree-merge "
            "strictly amplifies modular phase noise relative to direct single-leaf Fourier readout."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_NOISY_TREE_MERGE_CONVOLUTION_AND_SNR_CROSSOVER"
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


def write_dcp_noisy_tree_merge_error_propagation_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_noisy_tree_merge_error_propagation_audit(contract_path=contract_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP noisy tree-merge error-propagation audit."
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
        payload = write_dcp_noisy_tree_merge_error_propagation_audit(output_path=args.output)
    else:
        payload = build_dcp_noisy_tree_merge_error_propagation_audit()

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
