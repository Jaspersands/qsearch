from __future__ import annotations

import argparse
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


SCHEMA_VERSION = "2026-04-12.planted-qary-coset-shift-fourier-bias-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_coset_shift_fourier_bias_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_coset_shift_fourier_bias_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_COSET_SHIFT_FOURIER_BIAS_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_coset_shift_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    shift_a: list[int],
    window: list[int],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Exhaustively verify Theorems 1, 2, and 3 on F_q^n for subspace B = rowspan(M) and coset B + a."""
    M = np.array(generator_matrix, dtype=int) % q
    d, n_cols = M.shape
    if n_cols != n:
        raise ValueError("generator_matrix column count must equal n")
    a_vec = np.array(shift_a, dtype=int) % q
    R = len(window)
    window_set = set(window)
    zero_in_window = 0 in window_set

    # Enumerate all x in F_q^n (ordered lexicographically)
    all_vectors = [ np.array(v, dtype=int) for v in itertools.product(range(q), repeat=n) ]
    vec_to_idx = {tuple(v.tolist()): idx for idx, v in enumerate(all_vectors)}
    N_total = q ** n

    # Construct B = {c^T M mod q : c in F_q^d} and coset B + a
    B_set: set[tuple[int, ...]] = set()
    for c in itertools.product(range(q), repeat=d):
        c_arr = np.array(c, dtype=int)
        b_vec = tuple(((c_arr @ M) % q).tolist())
        B_set.add(b_vec)
    if len(B_set) != q ** d:
        raise ValueError("generator_matrix does not have full row rank d")

    a_tuple = tuple(a_vec.tolist())
    a_in_B = a_tuple in B_set
    coset_set = {tuple(((np.array(b, dtype=int) + a_vec) % q).tolist()) for b in B_set}

    # Construct dual subspace B^perp = {u in F_q^n : M u = 0 mod q}
    B_perp_set: set[tuple[int, ...]] = set()
    for u_vec in all_vectors:
        if np.all((M @ u_vec) % q == 0):
            B_perp_set.add(tuple(u_vec.tolist()))
    expected_dual_size = q ** (n - d)
    if len(B_perp_set) != expected_dual_size:
        raise ValueError("Dual subspace size mismatch")

    # 1. Verify Theorem 1: Exact QFT_q^{\otimes n} amplitude & Born distribution on |psi_{B+a}> vs |psi_B>
    # Direct Fourier transform over F_q^n: <u | QFT_q^{\otimes n} | psi_{B+a}> = q^{-(n+d)/2} sum_{x in B+a} omega_q^{<u, x>}
    qft_born_coset = np.zeros(N_total, dtype=np.float64)
    qft_born_homogeneous = np.zeros(N_total, dtype=np.float64)
    max_qft_amp_formula_residual = 0.0
    norm_factor = float(q ** (-(n + d) / 2.0))
    theo_dual_amp_mag = float(q ** (-(n - d) / 2.0))

    for u_idx, u_vec in enumerate(all_vectors):
        u_tuple = tuple(u_vec.tolist())
        # Direct sum over B + a
        amp_coset = 0.0 + 0.0j
        for x_tuple in coset_set:
            dot_ux = int(np.dot(u_vec, np.array(x_tuple, dtype=int))) % q
            angle = 2.0 * math.pi * dot_ux / float(q)
            amp_coset += complex(math.cos(angle), math.sin(angle))
        amp_coset *= norm_factor
        qft_born_coset[u_idx] = amp_coset.real ** 2 + amp_coset.imag ** 2

        # Direct sum over B
        amp_hom = 0.0 + 0.0j
        for b_tuple in B_set:
            dot_ub = int(np.dot(u_vec, np.array(b_tuple, dtype=int))) % q
            angle = 2.0 * math.pi * dot_ub / float(q)
            amp_hom += complex(math.cos(angle), math.sin(angle))
        amp_hom *= norm_factor
        qft_born_homogeneous[u_idx] = amp_hom.real ** 2 + amp_hom.imag ** 2

        # Theoretical amplitude on |psi_{B+a}>:
        if u_tuple in B_perp_set:
            dot_au = int(np.dot(a_vec, u_vec)) % q
            angle_au = 2.0 * math.pi * dot_au / float(q)
            theo_amp = theo_dual_amp_mag * complex(math.cos(angle_au), math.sin(angle_au))
        else:
            theo_amp = 0.0 + 0.0j
        max_qft_amp_formula_residual = max(
            max_qft_amp_formula_residual, abs(amp_coset - theo_amp)
        )

    qft_tv_distance = 0.5 * float(np.sum(np.abs(qft_born_coset - qft_born_homogeneous)))
    theorem1_verified = (
        max_qft_amp_formula_residual <= tolerance and qft_tv_distance <= tolerance
    )

    # 2. Verify Theorem 2 & Theorem 3: Classical probe acceptance counts on B+a vs B across all u in F_q^n
    off_dual_expected_count = (q ** (d - 1)) * R
    off_dual_invariance_holds = True
    dual_collapse_holds = True
    total_accepted_coset = 0
    total_accepted_hom = 0
    dual_accepted_coset = 0

    for u_vec in all_vectors:
        u_tuple = tuple(u_vec.tolist())
        cnt_coset = sum(
            1
            for x_tuple in coset_set
            if (int(np.dot(np.array(x_tuple, dtype=int), u_vec)) % q) in window_set
        )
        cnt_hom = sum(
            1
            for b_tuple in B_set
            if (int(np.dot(np.array(b_tuple, dtype=int), u_vec)) % q) in window_set
        )
        total_accepted_coset += cnt_coset
        total_accepted_hom += cnt_hom

        if u_tuple not in B_perp_set:
            if cnt_coset != off_dual_expected_count or cnt_hom != off_dual_expected_count:
                off_dual_invariance_holds = False
        else:
            dual_accepted_coset += cnt_coset
            dot_au = int(np.dot(a_vec, u_vec)) % q
            expected_dual_cnt = (q ** d) if (dot_au in window_set) else 0
            if cnt_coset != expected_dual_cnt:
                dual_collapse_holds = False

    theorem2_verified = off_dual_invariance_holds and dual_collapse_holds

    # Verify Theorem 3: Exact first-moment dichotomy
    emp_first_moment_coset = Fraction(total_accepted_coset, N_total)
    emp_first_moment_hom = Fraction(total_accepted_hom, N_total)
    theo_first_moment_hom = (
        (Fraction(1, 1) if zero_in_window else Fraction(0, 1))
        + Fraction(q ** d - 1, 1) * Fraction(R, q)
    )
    if a_in_B:
        theo_first_moment_coset = theo_first_moment_hom
    else:
        theo_first_moment_coset = Fraction((q ** (d - 1)) * R, 1)

    theorem3_verified = (
        emp_first_moment_hom == theo_first_moment_hom
        and emp_first_moment_coset == theo_first_moment_coset
    )

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "R": R,
        "window": list(window),
        "zero_in_window": zero_in_window,
        "shift_a": list(shift_a),
        "shift_a_in_B": a_in_B,
        "subspace_size_q_pow_d": q ** d,
        "dual_subspace_size_q_pow_n_minus_d": expected_dual_size,
        "max_qft_amplitude_formula_residual": max_qft_amp_formula_residual,
        "qft_born_tv_distance_coset_vs_subspace": qft_tv_distance,
        "off_dual_expected_acceptance_count": off_dual_expected_count,
        "off_dual_invariance_holds": off_dual_invariance_holds,
        "dual_collapse_holds": dual_collapse_holds,
        "homogeneous_first_moment_exact": _frac_str(emp_first_moment_hom),
        "homogeneous_first_moment_float": float(emp_first_moment_hom),
        "coset_first_moment_exact": _frac_str(emp_first_moment_coset),
        "coset_first_moment_float": float(emp_first_moment_coset),
        "theoretical_coset_first_moment_exact": _frac_str(theo_first_moment_coset),
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_planted_qary_coset_shift_fourier_bias_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n3_d2_nontrivial_coset_zerofree_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "shift_a": [0, 0, 1],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n3_d2_nontrivial_coset_with_zero_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "shift_a": [0, 0, 1],
            "window": [0, 1],
        },
        {
            "case_id": "q3_n3_d2_trivial_coset_a_in_B_zerofree_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "shift_a": [1, 1, 2],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n4_d2_nontrivial_coset_zerofree_R1",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "shift_a": [0, 0, 1, 0],
            "window": [1],
        },
        {
            "case_id": "q5_n3_d2_nontrivial_coset_zerofree_R2",
            "q": 5,
            "n": 3,
            "generator_matrix": [[1, 0, 2], [0, 1, 3]],
            "shift_a": [0, 0, 1],
            "window": [1, 4],
        },
    ]

    cases = [evaluate_coset_shift_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_qft_amplitude_formula_residual": max(
            c["max_qft_amplitude_formula_residual"] for c in cases
        ),
        "max_qft_born_tv_distance": max(
            c["qft_born_tv_distance_coset_vs_subspace"] for c in cases
        ),
        "scientific_verdict": (
            "Exhaustive verification across F_q^n confirms three exact properties of affine coset states "
            "B + a: (1) QFT_q^{\\otimes n} |psi_{B+a}> is supported strictly on B^perp with phases omega_q^{<a, u>}, "
            "so computational-basis measurement erases the coset shift a with zero total variation distance; "
            "(2) for every off-dual classical probe u not in B^perp, the window acceptance count N_W(u; B+a) = q^{d-1} R "
            "is deterministically invariant under all shifts a in F_q^n; and (3) for every non-trivial coset shift "
            "a not in B, averaging over u in F_q^n equalizes the first-moment acceptance count to exactly q^{d-1} R "
            "regardless of whether 0 in W."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_COSET_SHIFT_FOURIER_AND_PROBE_INVARIANCE"
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


def write_planted_qary_coset_shift_fourier_bias_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_coset_shift_fourier_bias_bridge(contract_path=contract_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary coset-shift Fourier-bias bridge."
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
        payload = write_planted_qary_coset_shift_fourier_bias_bridge(output_path=args.output)
    else:
        payload = build_planted_qary_coset_shift_fourier_bias_bridge()

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
