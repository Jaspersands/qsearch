from __future__ import annotations

import argparse
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
    signed_net_frequency,
)


SCHEMA_VERSION = "2026-04-12.native-higher-call-word-permutation-covariance-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "native_higher_call_word_permutation_covariance_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "native_higher_call_word_permutation_covariance_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_WORD_PERMUTATION_COVARIANCE_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_dilation_matrix(D: int, m: int) -> np.ndarray:
    """Return permutation matrix Pi_m where Pi_m |w> = |(m * w) mod D>."""
    if math.gcd(m, D) != 1:
        raise ValueError("m must be coprime to D")
    P = np.zeros((D, D), dtype=np.complex128)
    for w in range(D):
        P[(m * w) % D, w] = 1.0
    return P


def alternating_dilation_statevector(
    D: int,
    q: int,
    y_phases: list[int],
    m: int,
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
) -> np.ndarray:
    """Compute k-call state where odd calls use y^{(m)} and even calls use y^{(m^{-1})}."""
    m_inv = pow(m, -1, D)
    y_m = np.array([y_phases[(m * w) % D] for w in range(D)], dtype=np.float64)
    y_minv = np.array([y_phases[(m_inv * w) % D] for w in range(D)], dtype=np.float64)

    state = np.ones(D, dtype=np.complex128) / math.sqrt(float(D))
    for ell in range(len(epsilon)):
        y_step = y_m if (ell % 2 == 0) else y_minv
        diag_phase = np.exp(epsilon[ell] * 2j * np.pi * y_step / float(q))
        state = diag_phase * state
        F_step = fourier_matrix_power(D, sigma[ell])
        state = F_step @ state
    return state


def variety_size_for_freq_table(
    D: int,
    q: int,
    freq_table: list[tuple[int, ...]],
    epsilon: tuple[int, ...],
) -> int:
    k = len(epsilon)
    trajectories = list(itertools.product(range(D), repeat=k))
    taus = [signed_net_frequency(w, freq_table, epsilon, q) for w in trajectories]
    return sum(1 for a in range(len(taus)) for b in range(len(taus)) if taus[a] == taus[b])


def evaluate_word_permutation_case(
    *,
    case_id: str,
    D: int,
    q: int,
    n: int,
    m_unit: int,
    shift_b: int,
    freq_table: list[tuple[int, ...]],
    error_table: list[int],
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on dilation unit m_unit in Z_D^* and shift_b in Z_D."""
    k = len(epsilon)
    m_inv = pow(m_unit, -1, D)
    is_involutive = ((m_unit * m_unit) % D == 1)

    # 1. Verify Fourier-dilation intertwining: F_D^{sigma_l} Pi_m == Pi_{m^{-1}} F_D^{sigma_l}
    Pi_m = build_dilation_matrix(D, m_unit)
    Pi_minv = build_dilation_matrix(D, m_inv)
    F_plus = fourier_matrix_power(D, 1)
    F_minus = fourier_matrix_power(D, -1)
    intertwine_residual = max(
        float(np.max(np.abs((F_plus @ Pi_m) - (Pi_minv @ F_plus)))),
        float(np.max(np.abs((F_minus @ Pi_m) - (Pi_minv @ F_minus)))),
    )

    # Permuted frequency tables and collision variety sizes
    f_dilated = [freq_table[(m_unit * w) % D] for w in range(D)]
    f_shifted = [freq_table[(w + shift_b) % D] for w in range(D)]
    v_size_orig = variety_size_for_freq_table(D, q, freq_table, epsilon)
    v_size_dilated = variety_size_for_freq_table(D, q, f_dilated, epsilon)
    v_size_shifted = variety_size_for_freq_table(D, q, f_shifted, epsilon)
    variety_invariance_holds = (
        v_size_orig == v_size_dilated and v_size_orig == v_size_shifted
    )

    # Evaluate across all secrets s in Z_q^n
    secrets = list(itertools.product(range(q), repeat=n))
    max_involutive_or_k1_dilation_residual = 0.0
    max_alternating_intertwine_residual = 0.0
    max_uniform_dilation_ordered_tv = 0.0
    max_shift_born_tv = 0.0

    for s in secrets:
        y_orig = [
            (sum(freq_table[w][j] * s[j] for j in range(n)) + error_table[w]) % q
            for w in range(D)
        ]
        y_dilated = [y_orig[(m_unit * w) % D] for w in range(D)]
        y_shifted = [y_orig[(w + shift_b) % D] for w in range(D)]

        psi_orig = k_call_statevector(D, q, y_orig, epsilon, sigma)
        psi_unif_dil = k_call_statevector(D, q, y_dilated, epsilon, sigma)
        psi_alt_dil = alternating_dilation_statevector(
            D, q, y_orig, m_unit, epsilon, sigma
        )
        psi_shift = k_call_statevector(D, q, y_shifted, epsilon, sigma)

        # Target state under alternating dilation: Pi_m |psi_orig> if k odd, Pi_{m^{-1}} |psi_orig> if k even
        expected_alt_psi = (Pi_m @ psi_orig) if (k % 2 == 1) else (Pi_minv @ psi_orig)
        alt_res = float(np.max(np.abs(psi_alt_dil - expected_alt_psi)))
        max_alternating_intertwine_residual = max(
            max_alternating_intertwine_residual, alt_res
        )

        # If m is involutive (or k == 1), uniform dilation equals Pi_m |psi_orig>
        if is_involutive or k == 1:
            unif_res = float(np.max(np.abs(psi_unif_dil - (Pi_m @ psi_orig))))
            max_involutive_or_k1_dilation_residual = max(
                max_involutive_or_k1_dilation_residual, unif_res
            )

        # Compare sorted Born distributions under uniform dilation vs original
        born_orig = np.abs(psi_orig) ** 2
        born_unif_dil = np.abs(psi_unif_dil) ** 2
        sorted_tv = 0.5 * float(
            np.sum(np.abs(np.sort(born_orig) - np.sort(born_unif_dil)))
        )
        max_uniform_dilation_ordered_tv = max(
            max_uniform_dilation_ordered_tv, sorted_tv
        )

        # Compare Born distributions under cyclic translation y^{[+b]}
        born_shift = np.abs(psi_shift) ** 2
        shift_tv = 0.5 * float(np.sum(np.abs(born_orig - born_shift)))
        max_shift_born_tv = max(max_shift_born_tv, shift_tv)

    theorem1_verified = bool(
        intertwine_residual <= tolerance
        and variety_invariance_holds
        and (
            max_involutive_or_k1_dilation_residual <= tolerance
            if (is_involutive or k == 1)
            else True
        )
    )

    if not is_involutive and k >= 2:
        # Must break sorted Born equivalence while alternating dilation rescues it
        theorem2_verified = bool(
            max_alternating_intertwine_residual <= tolerance
            and max_uniform_dilation_ordered_tv > 1e-4
        )
    else:
        theorem2_verified = bool(
            max_alternating_intertwine_residual <= tolerance
            and max_uniform_dilation_ordered_tv <= tolerance
        )

    if k == 1:
        theorem3_verified = bool(max_shift_born_tv <= tolerance)
    else:
        theorem3_verified = bool(
            max_shift_born_tv > 1e-4 if (shift_b % D != 0) else True
        )

    return {
        "case_id": case_id,
        "D": D,
        "q": q,
        "n": n,
        "k_calls": k,
        "m_unit": m_unit,
        "m_inv": m_inv,
        "is_involutive_m_sq_eq_1": is_involutive,
        "shift_b": shift_b,
        "variety_size_orig": v_size_orig,
        "variety_size_dilated": v_size_dilated,
        "variety_size_shifted": v_size_shifted,
        "variety_invariance_holds": variety_invariance_holds,
        "intertwine_residual": intertwine_residual,
        "max_involutive_or_k1_dilation_residual": max_involutive_or_k1_dilation_residual,
        "max_alternating_intertwine_residual": max_alternating_intertwine_residual,
        "max_uniform_dilation_ordered_tv": max_uniform_dilation_ordered_tv,
        "max_shift_born_tv": max_shift_born_tv,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_native_higher_call_word_permutation_covariance_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "k1_D5_non_involutive_m2_shift1_invariant",
            "D": 5,
            "q": 3,
            "n": 1,
            "m_unit": 2,
            "shift_b": 1,
            "freq_table": [(1,), (2,), (0,), (1,), (2,)],
            "error_table": [0, 1, 2, 0, 1],
            "epsilon": (1,),
            "sigma": (1,),
        },
        {
            "case_id": "k2_D5_involutive_m4_shift1",
            "D": 5,
            "q": 3,
            "n": 1,
            "m_unit": 4,
            "shift_b": 1,
            "freq_table": [(1,), (2,), (0,), (1,), (2,)],
            "error_table": [0, 1, 2, 0, 1],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_D5_non_involutive_m2_symmetry_breaking_and_alternating_rescue",
            "D": 5,
            "q": 3,
            "n": 1,
            "m_unit": 2,
            "shift_b": 2,
            "freq_table": [(1,), (2,), (0,), (1,), (2,)],
            "error_table": [0, 1, 2, 0, 1],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k3_D5_involutive_m4_covariance",
            "D": 5,
            "q": 3,
            "n": 1,
            "m_unit": 4,
            "shift_b": 1,
            "freq_table": [(1,), (2,), (0,), (1,), (2,)],
            "error_table": [0, 1, 2, 0, 1],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
        {
            "case_id": "k3_D5_non_involutive_m3_symmetry_breaking_and_alternating_rescue",
            "D": 5,
            "q": 3,
            "n": 1,
            "m_unit": 3,
            "shift_b": 1,
            "freq_table": [(1,), (2,), (0,), (1,), (2,)],
            "error_table": [0, 1, 2, 0, 1],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
    ]

    cases = [evaluate_word_permutation_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_intertwine_residual": max(c["intertwine_residual"] for c in cases),
        "max_alternating_intertwine_residual": max(
            c["max_alternating_intertwine_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across k in {1, 2, 3} oracle calls on D = 5, F_D^{sigma_l} Pi_m = Pi_{m^{-1}} F_D^{sigma_l} "
            "holds for all units m in Z_D^*. At k = 1, the full affine group Z_D rtimes Z_D^* preserves "
            "the unordered Born distribution. At k >= 2, involutive units (m^2 == 1 mod D) commute with "
            "F_D^{+-1} and preserve the k-call physics, whereas non-involutive units (m^2 != 1 mod D) "
            "and cyclic shifts (b != 0 mod D) break unitary equivalence while preserving |V_epsilon(f)|, "
            "and alternating (m, m^{-1}) calls restores exact intertwining for all m in Z_D^*."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_WORD_PERMUTATION_COVARIANCE_AND_ALTERNATING_RESCUE"
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


def write_native_higher_call_word_permutation_covariance_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_word_permutation_covariance_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call word-permutation covariance audit."
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
        payload = write_native_higher_call_word_permutation_covariance_audit(
            output_path=args.output
        )
    else:
        payload = build_native_higher_call_word_permutation_covariance_audit()

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
