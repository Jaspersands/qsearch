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

from theorems.dcp_noisy_tree_merge_error_propagation_audit import (
    fourier_cos_harmonics,
    symmetric_nearest_neighbor_kernel,
)
from theorems.dcp_quadrature_conjugate_pair_holevo_audit import build_qubit_pair_state


SCHEMA_VERSION = "2026-04-12.dcp-two-copy-cnot-difference-alignment-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_two_copy_cnot_difference_alignment_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_two_copy_cnot_difference_alignment_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_TWO_COPY_CNOT_DIFFERENCE_ALIGNMENT_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_cnot_12() -> np.ndarray:
    """Return 4x4 CNOT_{1 -> 2} unitary matrix on two qubits."""
    return np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=np.complex128,
    )


def apply_cnot_and_project_target(
    rho1: np.ndarray,
    rho2: np.ndarray,
    z_outcome: int,
) -> tuple[float, np.ndarray]:
    """Apply CNOT_{1 -> 2} to rho1 tensor rho2, project target qubit onto |z><z|, and trace out target."""
    if z_outcome not in (0, 1):
        raise ValueError("z_outcome must be 0 or 1")
    cnot = build_cnot_12()
    joint = np.kron(rho1, rho2)
    after_cnot = cnot @ joint @ cnot.conj().T

    # Extract 2x2 unnormalized block on control qubit for target outcome z_outcome
    # Basis ordering: |0,0> (0), |0,1> (1), |1,0> (2), |1,1> (3)
    idxs = [0 + z_outcome, 2 + z_outcome]
    unnorm_block = after_cnot[np.ix_(idxs, idxs)]
    prob_z = float(np.real(np.trace(unnorm_block)))
    post_rho1 = unnorm_block / prob_z
    return prob_z, post_rho1


def evaluate_cnot_alignment_case(
    *,
    case_id: str,
    q: int,
    p_err: float,
    test_secret_s: int = 1,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Exhaustively evaluate all (q-1)^2 difference pairs (d1, d2) in {1, ..., q-1}^2 and verify Theorems 1, 2, 3."""
    kernel = symmetric_nearest_neighbor_kernel(q, p_err)
    harmonics = fourier_cos_harmonics(kernel)
    nonzero_harmonics = harmonics[1:]  # d = 1, ..., q-1
    purity_l2 = float(np.sum(kernel ** 2))

    max_prob_half_residual = 0.0
    max_branch_state_residual = 0.0
    diagonal_z1_annihilation_holds = True
    antidiagonal_z0_annihilation_holds = True

    active_yield_sum = 0.0
    total_pairs = (q - 1) * (q - 1)

    for d1 in range(1, q):
        lam1 = float(harmonics[d1])
        theta1 = 2.0 * math.pi * float((d1 * test_secret_s) % q) / float(q)
        rho1 = build_qubit_pair_state(theta1, lam1)

        for d2 in range(1, q):
            lam2 = float(harmonics[d2])
            theta2 = 2.0 * math.pi * float((d2 * test_secret_s) % q) / float(q)
            rho2 = build_qubit_pair_state(theta2, lam2)

            p_z0, post_z0 = apply_cnot_and_project_target(rho1, rho2, 0)
            p_z1, post_z1 = apply_cnot_and_project_target(rho1, rho2, 1)

            max_prob_half_residual = max(
                max_prob_half_residual,
                abs(p_z0 - 0.5),
                abs(p_z1 - 0.5),
            )

            d_plus = (d1 + d2) % q
            d_minus = (d1 - d2) % q
            lam_prod = lam1 * lam2

            theta_plus = 2.0 * math.pi * float((d_plus * test_secret_s) % q) / float(q)
            theta_minus = (
                2.0 * math.pi * float((d_minus * test_secret_s) % q) / float(q)
            )
            theo_z0 = build_qubit_pair_state(theta_plus, lam_prod)
            theo_z1 = build_qubit_pair_state(theta_minus, lam_prod)

            res_z0 = float(np.max(np.abs(post_z0 - theo_z0)))
            res_z1 = float(np.max(np.abs(post_z1 - theo_z1)))
            max_branch_state_residual = max(
                max_branch_state_residual, res_z0, res_z1
            )

            # Check Theorem 2: diagonal (d1 == d2) and anti-diagonal (d1 + d2 == q) phase annihilation
            if d_plus == 0:
                # On anti-diagonal, post_z0 off-diagonal entry must be purely real 0.5 * lam1 * lam2
                if abs(float(np.imag(post_z0[0, 1]))) > tolerance:
                    antidiagonal_z0_annihilation_holds = False
            if d_minus == 0:
                # On diagonal, post_z1 off-diagonal entry must be purely real 0.5 * lam1 * lam2
                if abs(float(np.imag(post_z1[0, 1]))) > tolerance:
                    diagonal_z1_annihilation_holds = False

            y_pair = 0.0
            if d_plus != 0:
                y_pair += 0.5 * (lam_prod ** 2)
            if d_minus != 0:
                y_pair += 0.5 * (lam_prod ** 2)
            active_yield_sum += y_pair

    emp_ensemble_yield = active_yield_sum / float(total_pairs)

    # Theorem 3 closed-form formulas:
    sum_lam_sq = float(np.sum(nonzero_harmonics ** 2))
    sum_lam_fourth = float(np.sum(nonzero_harmonics ** 4))
    parseval_sum_lam_sq = float(q) * purity_l2 - 1.0

    formula1_yield = ((sum_lam_sq ** 2) - sum_lam_fourth) / float(total_pairs)
    formula2_yield = ((parseval_sum_lam_sq ** 2) - sum_lam_fourth) / float(total_pairs)

    off_diag_pair_sum = 0.0
    for d1 in range(1, q):
        for d2 in range(1, q):
            if d1 != d2:
                off_diag_pair_sum += float((harmonics[d1] ** 2) * (harmonics[d2] ** 2))
    formula3_yield = off_diag_pair_sum / float(total_pairs)

    yield_formula_residual = max(
        abs(emp_ensemble_yield - formula1_yield),
        abs(emp_ensemble_yield - formula2_yield),
        abs(emp_ensemble_yield - formula3_yield),
    )

    theorem1_verified = bool(
        max_prob_half_residual <= tolerance and max_branch_state_residual <= tolerance
    )
    theorem2_verified = bool(
        diagonal_z1_annihilation_holds and antidiagonal_z0_annihilation_holds
    )
    theorem3_verified = bool(yield_formula_residual <= tolerance)

    return {
        "case_id": case_id,
        "q": q,
        "p_err": p_err,
        "test_secret_s": test_secret_s,
        "total_difference_pairs": total_pairs,
        "collision_purity_l2": purity_l2,
        "sum_lambda_sq": sum_lam_sq,
        "sum_lambda_fourth": sum_lam_fourth,
        "empirical_ensemble_active_yield": emp_ensemble_yield,
        "closed_form_ensemble_active_yield": formula2_yield,
        "off_diagonal_pair_ensemble_yield": formula3_yield,
        "max_prob_half_residual": max_prob_half_residual,
        "max_branch_state_residual": max_branch_state_residual,
        "yield_formula_residual": yield_formula_residual,
        "diagonal_z1_annihilation_holds": diagonal_z1_annihilation_holds,
        "antidiagonal_z0_annihilation_holds": antidiagonal_z0_annihilation_holds,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_dcp_two_copy_cnot_difference_alignment_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q7_odd_modulus_p020",
            "q": 7,
            "p_err": 0.20,
            "test_secret_s": 2,
        },
        {
            "case_id": "q8_even_modulus_p015",
            "q": 8,
            "p_err": 0.15,
            "test_secret_s": 3,
        },
        {
            "case_id": "q11_odd_modulus_p025",
            "q": 11,
            "p_err": 0.25,
            "test_secret_s": 4,
        },
        {
            "case_id": "q12_even_modulus_p030",
            "q": 12,
            "p_err": 0.30,
            "test_secret_s": 5,
        },
        {
            "case_id": "q16_even_modulus_p010",
            "q": 16,
            "p_err": 0.10,
            "test_secret_s": 3,
        },
    ]

    cases = [evaluate_cnot_alignment_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_prob_half_residual": max(c["max_prob_half_residual"] for c in cases),
        "max_branch_state_residual": max(c["max_branch_state_residual"] for c in cases),
        "max_yield_formula_residual": max(c["yield_formula_residual"] for c in cases),
        "scientific_verdict": (
            "Across odd and even moduli q in {7, 8, 11, 12, 16}, applying CNOT_{1 -> 2} to two noisy "
            "DCP pair states rho_{d_1}(s) tensor rho_{d_2}(s) yields equiprobable target outcomes "
            "Pr(z=0) = Pr(z=1) = 1/2, bifurcating into sum difference (d_1 + d_2) mod q on z=0 and "
            "difference (d_1 - d_2) mod q on z=1 with product visibility lambda_{d_1} lambda_{d_2}. "
            "The anti-diagonal z=0 loss and diagonal z=1 loss sum to sum_{d=1}^{q-1} lambda_d^4, "
            "leaving exact ensemble active visibility ((q ||K_eta||_2^2 - 1)^2 - sum_{d=1}^{q-1} lambda_d^4)/(q - 1)^2."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_TWO_COPY_CNOT_BIFURCATION_AND_YIELD_LAWS"
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


def write_dcp_two_copy_cnot_difference_alignment_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_two_copy_cnot_difference_alignment_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP two-copy CNOT difference-alignment audit."
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
        payload = write_dcp_two_copy_cnot_difference_alignment_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_two_copy_cnot_difference_alignment_audit()

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
