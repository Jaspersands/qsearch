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

from theorems.dcp_multi_harmonic_weighted_fisher_decoder_audit import (
    build_symmetric_rational_kernel,
)
from theorems.dcp_noisy_tree_merge_error_propagation_audit import fourier_cos_harmonics
from theorems.dcp_quadrature_conjugate_pair_holevo_audit import build_qubit_pair_state


SCHEMA_VERSION = "2026-04-12.dcp-cyclic-subgroup-quotient-aliasing-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_cyclic_subgroup_quotient_aliasing_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_cyclic_subgroup_quotient_aliasing_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_CYCLIC_SUBGROUP_QUOTIENT_ALIASING_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def euler_totient(m: int) -> int:
    return sum(1 for u in range(1, m + 1) if math.gcd(u, m) == 1)


def ramanujan_sum_exact(m: int, e: int) -> int:
    """Compute Ramanujan's sum c_m(e) = sum_{1 <= u <= m, gcd(u, m) = 1} cos(2*pi*u*e/m), which is an exact integer."""
    val = sum(
        math.cos(2.0 * math.pi * float(u * e) / float(m))
        for u in range(1, m + 1)
        if math.gcd(u, m) == 1
    )
    return int(round(val))


def fold_rational_kernel(k_fracs: list[Fraction], q: int, g: int) -> list[Fraction]:
    """Fold rational kernel on Z_q onto Z_{q/g}."""
    m = q // g
    return [
        sum((k_fracs[e_bar + k * m] for k in range(g)), Fraction(0, 1))
        for e_bar in range(m)
    ]


def evaluate_quotient_aliasing_case(
    *,
    case_id: str,
    q: int,
    kernel_kind: str,
    p_num: int,
    p_den: int,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 across all proper divisors g | q."""
    k_fracs = build_symmetric_rational_kernel(q, kernel_kind, p_num, p_den)
    k_float = np.array([float(v) for v in k_fracs], dtype=np.float64)
    harmonics_q = fourier_cos_harmonics(k_float)
    base_purity_exact = sum((v * v for v in k_fracs), Fraction(0, 1))

    proper_divisors = [g for g in range(1, q) if q % g == 0]
    divisor_rows = []
    totient_sum = 0
    max_coset_periodicity_residual = 0.0
    max_folded_visibility_residual = 0.0
    max_ramanujan_stratum_residual = 0.0
    max_subgroup_parseval_residual = 0.0
    monotone_purity_holds = True

    for g in proper_divisors:
        m = q // g
        phi_m = euler_totient(m)
        totient_sum += phi_m

        stratum_d = [d for d in range(1, q) if math.gcd(d, q) == g]
        if len(stratum_d) != phi_m:
            raise ValueError("Stratum cardinality does not match Euler totient")

        folded_fracs = fold_rational_kernel(k_fracs, q, g)
        folded_float = np.array([float(v) for v in folded_fracs], dtype=np.float64)
        harmonics_m = fourier_cos_harmonics(folded_float)

        # Theorem 1:
        # (a) Coset periodicity rho_d((s + k*m) mod q) == rho_d(s)
        # (b) Folded visibility identity lambda_d(K_eta) == lambda_{d/g}(K_eta^{(m)})
        for d in stratum_d:
            d_prime = d // g
            lam_q = float(harmonics_q[d])
            lam_m = float(harmonics_m[d_prime])
            max_folded_visibility_residual = max(
                max_folded_visibility_residual, abs(lam_q - lam_m)
            )
            for s in range(m):
                theta_0 = 2.0 * math.pi * float((d * s) % q) / float(q)
                rho_0 = build_qubit_pair_state(theta_0, lam_q)
                for k_step in range(1, g):
                    s_shift = (s + k_step * m) % q
                    theta_k = 2.0 * math.pi * float((d * s_shift) % q) / float(q)
                    rho_k = build_qubit_pair_state(theta_k, lam_q)
                    res_p = float(np.max(np.abs(rho_k - rho_0)))
                    max_coset_periodicity_residual = max(
                        max_coset_periodicity_residual, res_p
                    )

        # Theorem 2: Ramanujan sum identity for stratum visibility sum
        emp_stratum_sum = float(sum(harmonics_q[d] for d in stratum_d))
        ramanujan_exact = sum(
            (k_fracs[e] * Fraction(ramanujan_sum_exact(m, e), 1) for e in range(q)),
            Fraction(0, 1),
        )
        ram_res = abs(emp_stratum_sum - float(ramanujan_exact))
        max_ramanujan_stratum_residual = max(max_ramanujan_stratum_residual, ram_res)

        # Theorem 3: Subgroup Parseval identity for folded kernel purity
        folded_purity_exact = sum((v * v for v in folded_fracs), Fraction(0, 1))
        subgroup_parseval_float = (float(g) / float(q)) * float(
            sum(harmonics_q[k_idx * g] ** 2 for k_idx in range(m))
        )
        sub_res = abs(float(folded_purity_exact) - subgroup_parseval_float)
        max_subgroup_parseval_residual = max(max_subgroup_parseval_residual, sub_res)

        if folded_purity_exact < base_purity_exact:
            monotone_purity_holds = False

        divisor_rows.append(
            {
                "divisor_g": g,
                "quotient_order_m": m,
                "stratum_size_phi_m": phi_m,
                "stratum_differences": stratum_d,
                "stratum_visibility_sum_exact": _frac_str(ramanujan_exact),
                "stratum_visibility_sum_float": emp_stratum_sum,
                "folded_purity_exact": _frac_str(folded_purity_exact),
                "folded_purity_float": float(folded_purity_exact),
                "subgroup_parseval_float": subgroup_parseval_float,
            }
        )

    theorem1_verified = bool(
        max_coset_periodicity_residual <= tolerance
        and max_folded_visibility_residual <= tolerance
    )
    theorem2_verified = bool(
        totient_sum == (q - 1) and max_ramanujan_stratum_residual <= tolerance
    )
    theorem3_verified = bool(
        monotone_purity_holds and max_subgroup_parseval_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "q": q,
        "kernel_kind": kernel_kind,
        "p_param_exact": _frac_str(Fraction(p_num, p_den)),
        "base_purity_exact": _frac_str(base_purity_exact),
        "base_purity_float": float(base_purity_exact),
        "proper_divisor_count": len(proper_divisors),
        "totient_sum_q_minus_1": totient_sum,
        "max_coset_periodicity_residual": max_coset_periodicity_residual,
        "max_folded_visibility_residual": max_folded_visibility_residual,
        "max_ramanujan_stratum_residual": max_ramanujan_stratum_residual,
        "max_subgroup_parseval_residual": max_subgroup_parseval_residual,
        "monotone_purity_holds": monotone_purity_holds,
        "divisor_rows": divisor_rows,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_dcp_cyclic_subgroup_quotient_aliasing_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q6_composite_nearest_neighbor_p_1_over_4",
            "q": 6,
            "kernel_kind": "nearest_neighbor",
            "p_num": 1,
            "p_den": 4,
        },
        {
            "case_id": "q8_power_of_two_nearest_neighbor_p_1_over_3",
            "q": 8,
            "kernel_kind": "nearest_neighbor",
            "p_num": 1,
            "p_den": 3,
        },
        {
            "case_id": "q9_odd_prime_power_two_shell_p_2_over_5",
            "q": 9,
            "kernel_kind": "two_shell",
            "p_num": 2,
            "p_den": 5,
        },
        {
            "case_id": "q12_highly_composite_two_shell_p_1_over_2",
            "q": 12,
            "kernel_kind": "two_shell",
            "p_num": 1,
            "p_den": 2,
        },
        {
            "case_id": "q15_odd_semiprime_nearest_neighbor_p_1_over_5",
            "q": 15,
            "kernel_kind": "nearest_neighbor",
            "p_num": 1,
            "p_den": 5,
        },
    ]

    cases = [evaluate_quotient_aliasing_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_coset_periodicity_residual": max(
            c["max_coset_periodicity_residual"] for c in cases
        ),
        "max_folded_visibility_residual": max(
            c["max_folded_visibility_residual"] for c in cases
        ),
        "max_ramanujan_stratum_residual": max(
            c["max_ramanujan_stratum_residual"] for c in cases
        ),
        "max_subgroup_parseval_residual": max(
            c["max_subgroup_parseval_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across composite moduli q in {6, 8, 9, 12, 15} and all proper divisors g | q, "
            "each g-divisible DCP difference d = g d' induces exact (q/g)-periodicity in the secret s "
            "and folded-kernel visibility invariance lambda_d(K_eta) = lambda_{d'}(K_eta^{(q/g)}). "
            "The divisor strata have sizes phi(q/g) with visibility sums given by Ramanujan's sum "
            "sum_e K_eta(e) c_{q/g}(e), and the folded kernel purity equals (g/q) sum_{k=0}^{q/g-1} "
            "lambda_{k g}(K_eta)^2 >= ||K_eta||_2^2."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_QUOTIENT_ALIASING_AND_RAMANUJAN_STRATUM_LAWS"
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


def write_dcp_cyclic_subgroup_quotient_aliasing_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_cyclic_subgroup_quotient_aliasing_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP cyclic-subgroup quotient-aliasing audit."
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
        payload = write_dcp_cyclic_subgroup_quotient_aliasing_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_cyclic_subgroup_quotient_aliasing_audit()

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
