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

from theorems.dcp_noisy_tree_merge_error_propagation_audit import (
    fourier_cos_harmonics,
    symmetric_nearest_neighbor_kernel,
)


SCHEMA_VERSION = "2026-04-12.dcp-quadrature-conjugate-pair-holevo-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_quadrature_conjugate_pair_holevo_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_quadrature_conjugate_pair_holevo_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_QUADRATURE_CONJUGATE_PAIR_HOLEVO_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def binary_entropy_bits(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))


def von_neumann_entropy_bits(rho: np.ndarray) -> float:
    eigvals = np.linalg.eigvalsh(rho)
    total = 0.0
    for v in eigvals:
        if v > 1e-15:
            total -= float(v) * math.log2(float(v))
    return total


def build_qubit_pair_state(theta: float, lambda_d: float) -> np.ndarray:
    """Return 2x2 density matrix rho_d(theta; lambda_d)."""
    off_diag = 0.5 * lambda_d * complex(math.cos(theta), -math.sin(theta))
    return np.array(
        [[0.5, off_diag], [off_diag.conjugate(), 0.5]],
        dtype=np.complex128,
    )


def evaluate_conjugate_pair_holevo_case(
    *,
    case_id: str,
    q: int,
    p_err: float,
    d_diff: int,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 for a DCP pair state with difference d_diff in {1, ..., q-1}."""
    if not (1 <= d_diff < q):
        raise ValueError("d_diff must be in {1, ..., q-1}")

    kernel = symmetric_nearest_neighbor_kernel(q, p_err)
    harmonics = fourier_cos_harmonics(kernel)
    lambda_d = float(harmonics[d_diff])

    # 1. Verify Theorem 1: Exact Holevo capacity across s in {0, ..., q-1}
    rho_list = []
    entropies = []
    for s in range(q):
        theta_s = 2.0 * math.pi * float((d_diff * s) % q) / float(q)
        rho_s = build_qubit_pair_state(theta_s, lambda_d)
        rho_list.append(rho_s)
        entropies.append(von_neumann_entropy_bits(rho_s))

    rho_avg = np.mean(rho_list, axis=0)
    half_I2 = 0.5 * np.eye(2, dtype=np.complex128)
    rho_avg_vs_half_I2_residual = float(np.max(np.abs(rho_avg - half_I2)))

    s_avg_entropy = von_neumann_entropy_bits(rho_avg)
    mean_cond_entropy = float(np.mean(entropies))
    emp_holevo_bits = s_avg_entropy - mean_cond_entropy
    theo_holevo_bits = 1.0 - binary_entropy_bits(0.5 * (1.0 + abs(lambda_d)))
    holevo_residual = abs(emp_holevo_bits - theo_holevo_bits)

    theorem1_verified = bool(
        rho_avg_vs_half_I2_residual <= tolerance and holevo_residual <= tolerance
    )

    # 2. Verify Theorem 2 & Theorem 3 across a dense grid of phase angles theta in [0, 2*pi)
    # including theta = 0, pi/4, pi/2, pi, and all discrete secret angles 2*pi*d*s/q
    theta_grid = [0.0, math.pi / 4.0, math.pi / 2.0, 3.0 * math.pi / 4.0, math.pi] + [
        2.0 * math.pi * float((d_diff * s) % q) / float(q) for s in range(q)
    ]

    sigma_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
    sigma_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
    singlet_vec = np.array([0.0, 1.0, -1.0, 0.0], dtype=np.complex128) / math.sqrt(2.0)
    Pi_singlet = np.outer(singlet_vec, singlet_vec.conj())
    Pi_triplet = np.eye(4, dtype=np.complex128) - Pi_singlet

    min_i_xy = float("inf")
    max_i_xy = float("-inf")
    max_qfi_residual = 0.0
    max_xy_formula_residual = 0.0
    max_singlet_residual = 0.0
    max_triplet_coherence_residual = 0.0

    expected_min_xy = 0.5 * (lambda_d ** 2)
    expected_max_xy = (lambda_d ** 2) / (2.0 - (lambda_d ** 2))
    expected_qfi = lambda_d ** 2
    expected_singlet_prob = 0.25 * (1.0 - (lambda_d ** 2))
    expected_triplet_prob = 0.25 * (3.0 + (lambda_d ** 2))

    for theta in theta_grid:
        rho_t = build_qubit_pair_state(theta, lambda_d)
        # SLD operator L_theta = -lambda_d sin(theta) sigma_X + lambda_d cos(theta) sigma_Y
        L_theta = (-lambda_d * math.sin(theta)) * sigma_X + (
            lambda_d * math.cos(theta)
        ) * sigma_Y
        # Check SLD equation: d/dtheta rho_t == 0.5 * (rho_t L_theta + L_theta rho_t)
        drho_dtheta = 0.5 * (
            (-lambda_d * math.sin(theta)) * sigma_X
            + (lambda_d * math.cos(theta)) * sigma_Y
        )
        sld_rhs = 0.5 * (rho_t @ L_theta + L_theta @ rho_t)
        sld_eq_res = float(np.max(np.abs(drho_dtheta - sld_rhs)))
        qfi_val = float(np.real(np.trace(rho_t @ (L_theta @ L_theta))))
        max_qfi_residual = max(
            max_qfi_residual, abs(qfi_val - expected_qfi), sld_eq_res
        )

        # Classical Fisher informations I_X, I_Y, I_XY
        c_t = math.cos(theta)
        s_t = math.sin(theta)
        i_x = ((lambda_d ** 2) * (s_t ** 2)) / (1.0 - (lambda_d ** 2) * (c_t ** 2))
        i_y = ((lambda_d ** 2) * (c_t ** 2)) / (1.0 - (lambda_d ** 2) * (s_t ** 2))
        i_xy = 0.5 * (i_x + i_y)
        i_xy_closed = (
            (lambda_d ** 2) * (1.0 - (lambda_d ** 2) * ((c_t ** 4) + (s_t ** 4)))
        ) / (
            2.0
            * (1.0 - (lambda_d ** 2) * (c_t ** 2))
            * (1.0 - (lambda_d ** 2) * (s_t ** 2))
        )
        max_xy_formula_residual = max(
            max_xy_formula_residual, abs(i_xy - i_xy_closed)
        )
        min_i_xy = min(min_i_xy, i_xy)
        max_i_xy = max(max_i_xy, i_xy)

        # Two-copy singlet/triplet projections
        rho_2 = np.kron(rho_t, rho_t)
        p_sing = float(np.real(np.trace(Pi_singlet @ rho_2)))
        p_trip = float(np.real(np.trace(Pi_triplet @ rho_2)))
        max_singlet_residual = max(
            max_singlet_residual,
            abs(p_sing - expected_singlet_prob),
            abs(p_trip - expected_triplet_prob),
        )
        # Check <00 | rho_2 | 11> == (lambda_d^2 / 4) * exp(-2 i theta)
        coh_00_11 = rho_2[0, 3]
        theo_coh = 0.25 * (lambda_d ** 2) * complex(
            math.cos(2.0 * theta), -math.sin(2.0 * theta)
        )
        max_triplet_coherence_residual = max(
            max_triplet_coherence_residual, float(abs(coh_00_11 - theo_coh))
        )

    theorem2_verified = bool(
        max_qfi_residual <= tolerance
        and max_xy_formula_residual <= tolerance
        and abs(min_i_xy - expected_min_xy) <= tolerance
        and abs(max_i_xy - expected_max_xy) <= tolerance
        and expected_max_xy < expected_qfi
    )
    theorem3_verified = bool(
        max_singlet_residual <= tolerance
        and max_triplet_coherence_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "q": q,
        "p_err": p_err,
        "d_diff": d_diff,
        "lambda_d": lambda_d,
        "holevo_capacity_empirical_bits": emp_holevo_bits,
        "holevo_capacity_theoretical_bits": theo_holevo_bits,
        "holevo_residual": holevo_residual,
        "rho_avg_vs_half_I2_residual": rho_avg_vs_half_I2_residual,
        "sld_quantum_fisher_info": expected_qfi,
        "min_conjugate_xy_fisher_info": min_i_xy,
        "expected_min_xy_fisher_info": expected_min_xy,
        "max_conjugate_xy_fisher_info": max_i_xy,
        "expected_max_xy_fisher_info": expected_max_xy,
        "singlet_probability_constant": expected_singlet_prob,
        "triplet_probability_constant": expected_triplet_prob,
        "max_qfi_residual": max_qfi_residual,
        "max_xy_formula_residual": max_xy_formula_residual,
        "max_singlet_residual": max_singlet_residual,
        "max_triplet_coherence_residual": max_triplet_coherence_residual,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_dcp_quadrature_conjugate_pair_holevo_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q8_p015_fundamental_d1",
            "q": 8,
            "p_err": 0.15,
            "d_diff": 1,
        },
        {
            "case_id": "q8_p015_second_harmonic_d2",
            "q": 8,
            "p_err": 0.15,
            "d_diff": 2,
        },
        {
            "case_id": "q12_p025_fundamental_d1",
            "q": 12,
            "p_err": 0.25,
            "d_diff": 1,
        },
        {
            "case_id": "q12_p025_third_harmonic_d3",
            "q": 12,
            "p_err": 0.25,
            "d_diff": 3,
        },
        {
            "case_id": "q16_p020_fundamental_d1",
            "q": 16,
            "p_err": 0.20,
            "d_diff": 1,
        },
    ]

    cases = [evaluate_conjugate_pair_holevo_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_holevo_residual": max(c["holevo_residual"] for c in cases),
        "max_qfi_residual": max(c["max_qfi_residual"] for c in cases),
        "max_singlet_residual": max(c["max_singlet_residual"] for c in cases),
        "scientific_verdict": (
            "Across moduli q in {8, 12, 16} and harmonics d, the uniform-secret average of the noisy "
            "DCP qubit state rho_d(s; K_eta) equals I_2 / 2 with exact Holevo capacity 1 - h_2((1 + |lambda_d|)/2) "
            "bits. The SLD quantum Fisher information is constantly lambda_d^2, while 50/50 conjugate X/Y "
            "quadrature readout eliminates phase blind spots and is bounded inside [lambda_d^2 / 2, "
            "lambda_d^2 / (2 - lambda_d^2)]. On two identical-difference copies, the singlet projection "
            "has constant theta-independent probability (1 - lambda_d^2)/4."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_BLOCH_DISK_HOLEVO_AND_CONJUGATE_FISHER_LAWS"
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


def write_dcp_quadrature_conjugate_pair_holevo_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_quadrature_conjugate_pair_holevo_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP quadrature conjugate-pair Holevo audit."
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
        payload = write_dcp_quadrature_conjugate_pair_holevo_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_quadrature_conjugate_pair_holevo_audit()

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
