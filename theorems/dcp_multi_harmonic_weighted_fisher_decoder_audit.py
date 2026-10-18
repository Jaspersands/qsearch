from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_noisy_tree_merge_error_propagation_audit import fourier_cos_harmonics


SCHEMA_VERSION = "2026-04-12.dcp-multi-harmonic-weighted-fisher-decoder-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_multi_harmonic_weighted_fisher_decoder_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_multi_harmonic_weighted_fisher_decoder_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_MULTI_HARMONIC_WEIGHTED_FISHER_DECODER_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_symmetric_rational_kernel(
    q: int,
    kernel_kind: str,
    p_num: int,
    p_den: int,
) -> list[Fraction]:
    """Construct exact rational symmetric probability distribution K_eta on Z_q."""
    p_frac = Fraction(p_num, p_den)
    dist = [Fraction(0, 1) for _ in range(q)]
    if kernel_kind == "nearest_neighbor":
        dist[0] = Fraction(1, 1) - p_frac
        dist[1 % q] += p_frac / Fraction(2, 1)
        dist[(q - 1) % q] += p_frac / Fraction(2, 1)
    elif kernel_kind == "two_shell":
        # Weight 1 - p at 0, p/3 at +-1, p/6 at +-2
        dist[0] = Fraction(1, 1) - p_frac
        dist[1 % q] += p_frac / Fraction(3, 1)
        dist[(q - 1) % q] += p_frac / Fraction(3, 1)
        dist[2 % q] += p_frac / Fraction(6, 1)
        dist[(q - 2) % q] += p_frac / Fraction(6, 1)
    elif kernel_kind == "depolarizing":
        # Weight 1 - p at 0, and p / (q - 1) at every e in {1, ..., q-1}
        dist[0] = Fraction(1, 1) - p_frac
        rem = p_frac / Fraction(q - 1, 1)
        for e in range(1, q):
            dist[e] = rem
    else:
        raise ValueError(f"Unknown kernel_kind: {kernel_kind}")

    if sum(dist, Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("Kernel does not sum to 1")
    for e in range(q):
        if dist[e] != dist[(-e) % q]:
            raise ValueError("Kernel is not symmetric")
    return dist


def evaluate_multi_harmonic_case(
    *,
    case_id: str,
    q: int,
    kernel_kind: str,
    p_num: int,
    p_den: int,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a symmetric rational noise kernel K_eta on Z_q."""
    k_fracs = build_symmetric_rational_kernel(q, kernel_kind, p_num, p_den)
    k_float = np.array([float(v) for v in k_fracs], dtype=np.float64)

    harmonics = fourier_cos_harmonics(k_float)
    nonzero_harmonics = harmonics[1:]  # d = 1, ..., q-1

    # Theorem 1: sum_{d=1}^{q-1} lambda_d == q * K_eta(0) - 1
    emp_sum_lambda = float(np.sum(nonzero_harmonics))
    theo_sum_lambda_exact = Fraction(q, 1) * k_fracs[0] - Fraction(1, 1)
    theo_sum_lambda_float = float(theo_sum_lambda_exact)
    theorem1_residual = abs(emp_sum_lambda - theo_sum_lambda_float)
    theorem1_verified = theorem1_residual <= tolerance

    # Theorem 2: sum_{d=1}^{q-1} lambda_d^2 == q * sum_{e=0}^{q-1} K_eta(e)^2 - 1
    emp_sum_lambda_sq = float(np.sum(nonzero_harmonics ** 2))
    collision_purity_exact = sum((v * v for v in k_fracs), Fraction(0, 1))
    theo_sum_lambda_sq_exact = Fraction(q, 1) * collision_purity_exact - Fraction(1, 1)
    theo_sum_lambda_sq_float = float(theo_sum_lambda_sq_exact)
    theorem2_residual = abs(emp_sum_lambda_sq - theo_sum_lambda_sq_float)
    theorem2_verified = theorem2_residual <= tolerance

    # Theorem 3: Matched-harmonic SNR vs Uniform-weight SNR and exact physical-space gap
    snr_matched_emp = emp_sum_lambda_sq
    snr_matched_exact = theo_sum_lambda_sq_exact

    snr_unif_emp = (emp_sum_lambda ** 2) / float(q - 1)
    snr_unif_exact = (theo_sum_lambda_exact ** 2) / Fraction(q - 1, 1)

    snr_gap_emp = snr_matched_emp - snr_unif_emp
    snr_gap_exact = snr_matched_exact - snr_unif_exact

    # Physical-space non-zero error variance formula:
    # q * sum_{e=1}^{q-1} (K_eta(e) - (1 - K_eta(0))/(q - 1))^2
    mean_nonzero_err = (Fraction(1, 1) - k_fracs[0]) / Fraction(q - 1, 1)
    phys_gap_exact = Fraction(q, 1) * sum(
        ((k_fracs[e] - mean_nonzero_err) ** 2 for e in range(1, q)),
        Fraction(0, 1),
    )
    snr_gap_residual = abs(snr_gap_emp - float(phys_gap_exact))

    if kernel_kind == "depolarizing":
        gap_condition_holds = (snr_gap_exact == Fraction(0, 1))
    else:
        gap_condition_holds = (snr_gap_exact > Fraction(0, 1))

    theorem3_verified = (
        snr_gap_exact == phys_gap_exact
        and snr_gap_residual <= tolerance
        and gap_condition_holds
    )

    return {
        "case_id": case_id,
        "q": q,
        "kernel_kind": kernel_kind,
        "p_param_exact": _frac_str(Fraction(p_num, p_den)),
        "k0_zero_error_prob_exact": _frac_str(k_fracs[0]),
        "collision_purity_exact": _frac_str(collision_purity_exact),
        "collision_purity_float": float(collision_purity_exact),
        "nonzero_harmonic_sum_empirical": emp_sum_lambda,
        "nonzero_harmonic_sum_exact": _frac_str(theo_sum_lambda_exact),
        "nonzero_harmonic_sum_float": theo_sum_lambda_float,
        "nonzero_harmonic_sq_sum_empirical": emp_sum_lambda_sq,
        "nonzero_harmonic_sq_sum_exact": _frac_str(theo_sum_lambda_sq_exact),
        "nonzero_harmonic_sq_sum_float": theo_sum_lambda_sq_float,
        "snr_matched_exact": _frac_str(snr_matched_exact),
        "snr_matched_float": float(snr_matched_exact),
        "snr_uniform_exact": _frac_str(snr_unif_exact),
        "snr_uniform_float": float(snr_unif_exact),
        "snr_gap_matched_minus_uniform_exact": _frac_str(snr_gap_exact),
        "snr_gap_physical_variance_formula_exact": _frac_str(phys_gap_exact),
        "snr_gap_float": float(snr_gap_exact),
        "theorem1_residual": theorem1_residual,
        "theorem2_residual": theorem2_residual,
        "snr_gap_residual": snr_gap_residual,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_dcp_multi_harmonic_weighted_fisher_decoder_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q8_nearest_neighbor_p_1_over_4",
            "q": 8,
            "kernel_kind": "nearest_neighbor",
            "p_num": 1,
            "p_den": 4,
        },
        {
            "case_id": "q12_nearest_neighbor_p_1_over_3",
            "q": 12,
            "kernel_kind": "nearest_neighbor",
            "p_num": 1,
            "p_den": 3,
        },
        {
            "case_id": "q12_two_shell_p_3_over_5",
            "q": 12,
            "kernel_kind": "two_shell",
            "p_num": 3,
            "p_den": 5,
        },
        {
            "case_id": "q16_two_shell_p_1_over_2",
            "q": 16,
            "kernel_kind": "two_shell",
            "p_num": 1,
            "p_den": 2,
        },
        {
            "case_id": "q9_depolarizing_isotropic_p_2_over_5",
            "q": 9,
            "kernel_kind": "depolarizing",
            "p_num": 2,
            "p_den": 5,
        },
    ]

    cases = [evaluate_multi_harmonic_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_theorem1_residual": max(c["theorem1_residual"] for c in cases),
        "max_theorem2_residual": max(c["theorem2_residual"] for c in cases),
        "max_snr_gap_residual": max(c["snr_gap_residual"] for c in cases),
        "scientific_verdict": (
            "Across nearest-neighbor, two-shell, and isotropic depolarizing modular noise kernels on Z_q, "
            "the non-zero difference visibilities {lambda_d}_{d=1}^{q-1} satisfy sum_{d=1}^{q-1} lambda_d = "
            "q * K_eta(0) - 1 and sum_{d=1}^{q-1} lambda_d^2 = q * ||K_eta||_2^2 - 1. Matched-harmonic "
            "weighting w_d^* = lambda_d achieves SNR_matched = q * ||K_eta||_2^2 - 1 and strictly outperforms "
            "uniform difference weighting whenever K_eta is non-uniform on Z_q \\ {0}, with an exact SNR gap "
            "equal to q * sum_{e=1}^{q-1} (K_eta(e) - (1 - K_eta(0))/(q - 1))^2."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_MULTI_HARMONIC_PARSEVAL_AND_MATCHED_FILTER_LAWS"
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


def write_dcp_multi_harmonic_weighted_fisher_decoder_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_multi_harmonic_weighted_fisher_decoder_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP multi-harmonic weighted Fisher decoder audit."
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
        payload = write_dcp_multi_harmonic_weighted_fisher_decoder_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_multi_harmonic_weighted_fisher_decoder_audit()

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
