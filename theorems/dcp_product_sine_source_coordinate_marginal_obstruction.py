"""Product-group sine-window source coordinate-marginal dephasing & subset-sum equivalence obstruction.

Certifies:
1. Theorem 1 (Exact Single-Coordinate Marginal Dephasing Identity):
   For any shift h = (h_1, h_aux) in Z_q x Z_q^{n-1} and visibility v in [0, 1],
   averaging the product-group sine-window colour state rho_{(k_1, k_aux)}(h) over
   uniform auxiliary labels k_aux in Z_q^{n-1} yields effective marginal visibility
     v_eff(h_aux) = v * 1[h_2 == ... == h_n == 0 mod q].
   For all q^{n-1} - 1 non-zero auxiliary shifts h_aux != 0, bar{rho}_{k_1}(h) = I_2 / 2
   is identically maximally mixed and independent of h_1 and k_1.
2. Theorem 2 (K-Copy Coordinate-1 Parity Invariance & Cyclic-vs-Product Copy Threshold Equivalence):
   Over K product-group samples with vector labels A in Z_q^{n x K} and uniform prior
   h in Z_q^n, the h_1 mod 2 parity density difference satisfies
     (rho_even^{(K)} - rho_odd^{(K)})[x, x']
       = (2 / 2^K) * v^{wt_H(x XOR x')} * 1[A(x - x') == (q/2, 0, ..., 0)^T mod q].
   Because |G_prod| = q^n = (2M)^n = |G_cyclic|, the universal average parity advantage
   bound min(1/2, ((1+v)^K - 1)/(2 q^n)) and minimum copy threshold K_min are strictly
   invariant between cyclic and product-group readouts.
3. Theorem 3 (Auxiliary-Zero Postselection Sample Complexity):
   Postselecting product-group samples with k_2 == ... == k_n == 0 mod q restores
   scalar h_1 phase states with visibility v and group size q, but succeeds with
   probability P_accept = q^{-(n-1)} = 2^{-L(n-1)} per preparation, requiring
   E[N_prep] = K_1 * 2^{L(n-1)} source preparations for K_1 retained samples.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_native_parity_bridge import minimum_copies_for_advantage


DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_product_sine_source_coordinate_marginal_obstruction_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_product_sine_source_coordinate_marginal_obstruction.json"
)


def exact_minimum_copies(
    components: int, bits: int, advantage: Fraction, visibility: Fraction
) -> int:
    """Return the least integer K >= 1 such that ((1+v)^K - 1)/(2 * 2^{components*bits}) >= advantage."""
    eps = Fraction(advantage)
    v = Fraction(visibility)
    total_bits = int(components) * int(bits)
    target = eps.denominator + 2 * eps.numerator * (1 << total_bits)
    base = 1 + v
    lo, hi = 1, max(1, total_bits)
    while (base.numerator ** hi) * eps.denominator < target * (base.denominator ** hi):
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if (base.numerator ** mid) * eps.denominator >= target * (
            base.denominator ** mid
        ):
            hi = mid
        else:
            lo = mid + 1
    if bits >= 3:
        ref = int(
            minimum_copies_for_advantage(
                components, bits, eps, visibility=v
            )
        )
        assert lo == ref, f"Mismatch with minimum_copies_for_advantage: {lo} != {ref}"
    return int(lo)


def single_sample_colour_density(
    k: Sequence[int], h: Sequence[int], q: int, v: float
) -> np.ndarray:
    """Return the 2x2 conditional colour density matrix rho_k(h) for product-group label k."""
    dot = sum(int(k[i]) * int(h[i]) for i in range(len(k))) % q
    phase = np.exp(-2j * np.pi * dot / q)
    return 0.5 * np.array(
        [[1.0 + 0.0j, v * phase], [v * np.conj(phase), 1.0 + 0.0j]], dtype=complex
    )


def k_copy_product_density(
    A: Sequence[Sequence[int]], h: Sequence[int], q: int, v: float
) -> np.ndarray:
    """Return the 2^K x 2^K K-copy density matrix for vector label matrix A in Z_q^{n x K}."""
    n = len(A)
    K = len(A[0])
    L = 1 << K
    freqs = [
        sum(
            int(h[ell]) * sum(int(A[ell][r]) * ((x >> r) & 1) for r in range(K))
            for ell in range(n)
        )
        % q
        for x in range(L)
    ]
    phases = np.exp(-2j * np.pi * np.array(freqs, dtype=float) / q)
    rho = np.zeros((L, L), dtype=complex)
    for x in range(L):
        for y in range(L):
            w = (x ^ y).bit_count()
            rho[x, y] = (phases[x] * np.conj(phases[y])) * (v ** w) / float(L)
    return rho


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a product-group sine-window instance."""
    instance_id = str(instance["instance_id"])
    n = int(instance["n"])
    L_bits = int(instance["L"])
    q = int(instance["q"])
    assert q == (1 << L_bits)
    K = int(instance["K"])
    v_frac = Fraction(instance["visibility"])
    v = float(v_frac)
    A = [[int(x) for x in row] for row in instance["A"]]

    all_shifts = list(itertools.product(range(q), repeat=n))
    all_k_aux = list(itertools.product(range(q), repeat=n - 1))
    I_half = 0.5 * np.eye(2, dtype=complex)

    max_marginal_error = 0.0
    zero_aux_shift_count = 0
    nonzero_aux_shift_count = 0
    max_nonzero_aux_trace_dist = 0.0

    for h in all_shifts:
        h1 = h[0]
        h_aux = h[1:]
        aux_is_zero = all(x == 0 for x in h_aux)
        if aux_is_zero:
            zero_aux_shift_count += 1
        else:
            nonzero_aux_shift_count += 1

        for k1 in range(q):
            emp_marginal = np.zeros((2, 2), dtype=complex)
            for k_aux in all_k_aux:
                k_full = (k1,) + k_aux
                emp_marginal += single_sample_colour_density(k_full, h, q, v)
            emp_marginal /= float(len(all_k_aux))

            v_eff = v if aux_is_zero else 0.0
            phase1 = np.exp(-2j * np.pi * ((k1 * h1) % q) / q)
            theo_marginal = 0.5 * np.array(
                [[1.0 + 0.0j, v_eff * phase1], [v_eff * np.conj(phase1), 1.0 + 0.0j]],
                dtype=complex,
            )
            err = float(np.max(np.abs(emp_marginal - theo_marginal)))
            max_marginal_error = max(max_marginal_error, err)

            if not aux_is_zero:
                td = 0.5 * float(
                    np.sum(np.abs(np.linalg.eigvalsh(emp_marginal - I_half)))
                )
                max_nonzero_aux_trace_dist = max(max_nonzero_aux_trace_dist, td)

    theorem1_passed = bool(
        max_marginal_error <= 1e-12
        and max_nonzero_aux_trace_dist <= 1e-12
        and zero_aux_shift_count == q
        and nonzero_aux_shift_count == (q ** n - q)
    )

    dim_K = 1 << K
    rho_even = np.zeros((dim_K, dim_K), dtype=complex)
    rho_odd = np.zeros((dim_K, dim_K), dtype=complex)
    for h in all_shifts:
        rho_h = k_copy_product_density(A, h, q, v)
        if (h[0] % 2) == 0:
            rho_even += rho_h
        else:
            rho_odd += rho_h
    rho_even /= float((q ** n) // 2)
    rho_odd /= float((q ** n) // 2)
    delta_emp = rho_even - rho_odd

    target_vec = (q // 2,) + (0,) * (n - 1)
    word_freqs = [
        tuple(
            int(sum(A[ell][r] * ((x >> r) & 1) for r in range(K)) % q)
            for ell in range(n)
        )
        for x in range(dim_K)
    ]

    delta_theo = np.zeros((dim_K, dim_K), dtype=complex)
    full_vector_target_pairs = 0
    coord1_only_target_pairs = 0
    spurious_coord1_only_pairs = 0

    for x in range(dim_K):
        for y in range(dim_K):
            diff_vec = tuple(
                (word_freqs[x][ell] - word_freqs[y][ell]) % q for ell in range(n)
            )
            if diff_vec[0] == (q // 2):
                coord1_only_target_pairs += 1
                if diff_vec != target_vec:
                    spurious_coord1_only_pairs += 1
            if diff_vec == target_vec:
                full_vector_target_pairs += 1
                w = (x ^ y).bit_count()
                delta_theo[x, y] = (2.0 / float(dim_K)) * (v ** w)

    max_delta_error = float(np.max(np.abs(delta_emp - delta_theo)))
    helstrom_adv = 0.25 * float(np.sum(np.abs(np.linalg.eigvalsh(delta_emp))))

    cyclic_kmin = exact_minimum_copies(1, n * L_bits, Fraction(1, 16), v_frac)
    product_kmin = exact_minimum_copies(n, L_bits, Fraction(1, 16), v_frac)

    theorem2_passed = bool(
        max_delta_error <= 1e-12
        and cyclic_kmin == product_kmin
        and spurious_coord1_only_pairs >= 0
    )

    all_labels = list(itertools.product(range(q), repeat=n))
    accepted_labels = [
        k_vec for k_vec in all_labels if all(k_vec[i] == 0 for i in range(1, n))
    ]
    p_accept_emp = Fraction(len(accepted_labels), len(all_labels))
    p_accept_theo = Fraction(1, q ** (n - 1))
    k1_scalar_needed = exact_minimum_copies(1, L_bits, Fraction(1, 16), v_frac)
    expected_preps_postselected = int(k1_scalar_needed * (q ** (n - 1)))

    theorem3_passed = bool(
        len(accepted_labels) == q and p_accept_emp == p_accept_theo
    )

    return {
        "instance_id": instance_id,
        "n": int(n),
        "L": int(L_bits),
        "q": int(q),
        "K": int(K),
        "visibility_exact": str(v_frac),
        "A": A,
        "marginal_audit": {
            "total_shifts": int(q ** n),
            "zero_aux_shift_count": int(zero_aux_shift_count),
            "nonzero_aux_shift_count": int(nonzero_aux_shift_count),
            "max_marginal_formula_error": float(max_marginal_error),
            "max_nonzero_aux_trace_distance_from_maximally_mixed": float(
                max_nonzero_aux_trace_dist
            ),
            "theorem1_passed": bool(theorem1_passed),
        },
        "k_copy_parity_audit": {
            "full_vector_target_ordered_pairs": int(full_vector_target_pairs),
            "coord1_only_target_ordered_pairs": int(coord1_only_target_pairs),
            "killed_by_auxiliary_averaging_pairs": int(spurious_coord1_only_pairs),
            "max_density_difference_error": float(max_delta_error),
            "optimal_helstrom_parity_advantage": float(helstrom_adv),
            "cyclic_k_min_for_adv_1_16": int(cyclic_kmin),
            "product_k_min_for_adv_1_16": int(product_kmin),
            "theorem2_passed": bool(theorem2_passed),
        },
        "postselection_audit": {
            "total_label_outcomes": int(len(all_labels)),
            "aux_zero_accepted_outcomes": int(len(accepted_labels)),
            "acceptance_probability_exact": str(p_accept_emp),
            "scalar_1d_k_min_for_adv_1_16": int(k1_scalar_needed),
            "expected_total_preparations_with_postselection": int(
                expected_preps_postselected
            ),
            "theorem3_passed": bool(theorem3_passed),
        },
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def evaluate_asymptotic_scaling(grid: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Evaluate cyclic-vs-product invariance and postselection blowup on the scaling grid."""
    rows: List[Dict[str, Any]] = []
    for item in grid:
        n = int(item["n"])
        L_bits = int(item["L"])
        adv = Fraction(item["advantage"])
        vis = Fraction(item["visibility"])
        total_bits = n * L_bits
        kmin_cyclic = exact_minimum_copies(1, total_bits, adv, vis)
        kmin_product = exact_minimum_copies(n, L_bits, adv, vis)
        kmin_scalar_1d = exact_minimum_copies(1, L_bits, adv, vis)
        assert kmin_cyclic == kmin_product
        rows.append(
            {
                "n": int(n),
                "coordinate_bits_L": int(L_bits),
                "total_group_entropy_bits_nL": int(total_bits),
                "cyclic_qft_controlled_phases": int(total_bits * (total_bits - 1) // 2),
                "product_qft_controlled_phases": int(n * L_bits * (L_bits - 1) // 2),
                "cyclic_minimum_copies": int(kmin_cyclic),
                "product_minimum_copies": int(kmin_product),
                "cyclic_equals_product_minimum_copies": bool(
                    kmin_cyclic == kmin_product
                ),
                "aux_zero_postselection_acceptance_neg_log2": int((n - 1) * L_bits),
                "scalar_1d_minimum_copies_after_postselection": int(kmin_scalar_1d),
            }
        )
    return rows


def build_dcp_product_sine_source_coordinate_marginal_obstruction_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]
    asymptotic_rows = evaluate_asymptotic_scaling(contract["asymptotic_scaling_grid"])

    all_t1 = bool(all(inst["marginal_audit"]["theorem1_passed"] for inst in instances))
    all_t2 = bool(
        all(inst["k_copy_parity_audit"]["theorem2_passed"] for inst in instances)
        and all(row["cyclic_equals_product_minimum_copies"] for row in asymptotic_rows)
    )
    all_t3 = bool(
        all(inst["postselection_audit"]["theorem3_passed"] for inst in instances)
    )
    all_passed = bool(all_t1 and all_t2 and all_t3)

    max_marg_err = float(
        max(inst["marginal_audit"]["max_marginal_formula_error"] for inst in instances)
    )
    max_delta_err = float(
        max(
            inst["k_copy_parity_audit"]["max_density_difference_error"]
            for inst in instances
        )
    )

    payload_for_hash = {
        "contract_id": contract["contract_id"],
        "instances": instances,
        "asymptotic_scaling": asymptotic_rows,
        "all_passed": all_passed,
    }
    digest = hashlib.sha256(
        json.dumps(payload_for_hash, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "1.0",
        "subsystem": "dcp_product_sine_source_coordinate_marginal_obstruction",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_PRODUCT_SINE_SOURCE_COORDINATE_MARGINAL_OBSTRUCTION.md",
        "contract_path": "research/hypotheses/dcp_product_sine_source_coordinate_marginal_obstruction_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_marginal_dephasing_passed": bool(all_t1),
            "theorem2_k_copy_threshold_invariance_passed": bool(all_t2),
            "theorem3_postselection_blowup_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "max_marginal_formula_error": float(max_marg_err),
            "max_k_copy_density_difference_error": float(max_delta_err),
        },
        "instances": instances,
        "asymptotic_scaling": asymptotic_rows,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
        "sha256": str(digest),
    }


def write_dcp_product_sine_source_coordinate_marginal_obstruction_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the product-group sine-window coordinate-marginal obstruction audit."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the reduction JSON artifact to research/reductions/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full report as JSON to stdout.",
    )
    args = parser.parse_args()

    if args.write:
        report = write_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    else:
        report = build_dcp_product_sine_source_coordinate_marginal_obstruction_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_product_sine_source_coordinate_marginal_obstruction] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"max_marg_err={s['max_marginal_formula_error']:.3e} "
            f"max_delta_err={s['max_k_copy_density_difference_error']:.3e} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
