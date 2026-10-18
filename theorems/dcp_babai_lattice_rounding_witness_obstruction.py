"""Exact clean-DCP coordinate-rounding coverage audit, not an impossibility test.

Certifies:
1. Theorem 1 (Exact Coset Bijection & Fundamental Parallelepiped Vertex Identity):
   For any A in Z_{2^t}^{n x K} with an invertible n x n pivot block mod 2, the q-ary
   kernel lattice Lambda_q(A) = {z in Z^K : A z = 0 mod 2^t} has full rank K and
   determinant det(Lambda_q(A)) = 2^{nt}. For any LLL-reduced basis B_col in Z^{K x K}
   (columns generating Lambda_q(A)) and center c = (1/2, ..., 1/2)^T, exact rational
   Babai rounding
     z_Babai(t) = z_0(t) - B_col * floor(B_col^{-1}(z_0(t) - c) + 1/2)
   selects the unique integer point in P_c(B_col) = c + B_col[-1/2, 1/2)^K for each
   coset t in Z_{2^t}^n, and
     |{t in Z_{2^t}^n : z_Babai(t) in {0, 1}^K}| == |{0, 1}^K intersect P_c(B_col)|.
2. Theorem 2 (Exact Half-Integer l_infinity Box-Overflow Dichotomy):
   For every target t in Z_{2^t}^n, the centered residual e(t) = z_Babai(t) - c lies
   in (Z + 1/2)^K, so
     z_Babai(t) in {0, 1}^K     <=>  ||e(t)||_infinity == 1/2,
     z_Babai(t) notin {0, 1}^K  <=>  ||e(t)||_infinity >= 3/2.
3. Theorem 3 (Direct-Filter & Forward-SWAP Formula Under Coordinate Rounding):
   Plugging U_t|0> = |z_Babai(t)> into dcp_direct_witness_filter and
   dcp_forward_sampler_swap on K = nt + Delta clean phase qubits yields verified
   coverage beta_Babai(A) = |{0, 1}^K intersect P_c(B_col)| / 2^{nt}, direct-filter
   full-secret success 2^{-Delta} beta_Babai(A)^2, and forward-SWAP parity advantage
   Adv_SWAP^Babai(A) = |{t : ||e(t)||_inf == 1/2 and ||e((t+h) mod 2^t)||_inf == 1/2}| / (2 * 2^K).

The half-integer dichotomy does not imply that overflow occurs. Volume ratios
are not integer-point probabilities. This is coordinate rounding in a basis,
not the Gram-Schmidt nearest-plane algorithm. All-target enumeration is only a
finite calibration; it is not a scalable quantum decoder implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from flint import fmpq_mat, fmpz_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_clean_linear_witness_carry_obstruction import (
    invert_matrix_mod_2adic, solve_f2_right_inverse,
)
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_babai_lattice_rounding_witness_obstruction_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_babai_lattice_rounding_witness_obstruction.json"
)


def find_invertible_pivot_cols(
    A: Sequence[Sequence[int]], t: int
) -> Tuple[List[int], List[List[int]]]:
    """Find n column indices of A forming an invertible n x n block modulo 2^t."""
    n = len(A)
    K = len(A[0])
    # RREF exposes a pivot block without an exponential scan of column subsets.
    right_inverse = solve_f2_right_inverse([[int(v) % 2 for v in row] for row in A])
    cols = [c for c in range(K) if any(right_inverse[c])]
    sub = [[int(A[r][c]) for c in cols] for r in range(n)]
    return cols, invert_matrix_mod_2adic(sub, t)


def build_qary_kernel_lll_basis(
    A: Sequence[Sequence[int]], t: int
) -> Tuple[List[int], List[List[int]], List[List[int]], List[List[Fraction]]]:
    """Construct the q-ary kernel lattice Lambda_q(A), LLL-reduce its row basis,
    and return (piv_cols, R_piv, B_col, B_col_inv_frac).
    """
    n = len(A)
    K = len(A[0])
    q = 1 << t
    piv_cols, R_piv = find_invertible_pivot_cols(A, t)
    piv_set = set(piv_cols)
    free_cols = [c for c in range(K) if c not in piv_set]

    basis_rows: List[List[int]] = []
    for c_f in free_cols:
        row = [0] * K
        row[c_f] = 1
        for i in range(n):
            coeff = (-sum(R_piv[i][ell] * A[ell][c_f] for ell in range(n))) % q
            row[piv_cols[i]] = int(coeff)
        basis_rows.append(row)
    for c_p in piv_cols:
        row = [0] * K
        row[c_p] = int(q)
        basis_rows.append(row)

    fmat = fmpz_mat(basis_rows)
    det_val = abs(int(fmat.det()))
    if det_val != (q ** n):
        raise ArithmeticError(f"Expected det(Lambda_q(A)) = {q**n}, got {det_val}")

    lll_rows = [[int(x) for x in r] for r in fmat.lll().tolist()]
    for r in lll_rows:
        for ell in range(n):
            if sum(A[ell][c] * r[c] for c in range(K)) % q != 0:
                raise ArithmeticError("LLL basis vector not in kernel lattice")

    B_col = [[int(lll_rows[col][row]) for col in range(K)] for row in range(K)]
    inv_qmat = fmpq_mat(B_col).inv()
    B_col_inv_frac = [
        [
            Fraction(
                int(inv_qmat[row, col].numerator),
                int(inv_qmat[row, col].denominator),
            )
            for col in range(K)
        ]
        for row in range(K)
    ]
    return piv_cols, R_piv, B_col, B_col_inv_frac


def babai_round_exact(
    z0: Sequence[int],
    B_col: Sequence[Sequence[int]],
    B_col_inv_frac: Sequence[Sequence[Fraction]],
) -> Tuple[List[int], List[Fraction], List[Fraction]]:
    """Round z0 in Z^K into P_c(B_col) = c + B_col[-1/2, 1/2)^K using exact Fractions."""
    K = len(z0)
    half = Fraction(1, 2)
    shifted = [Fraction(int(z0[r]), 1) - half for r in range(K)]
    u = [
        sum((B_col_inv_frac[i][r] * shifted[r] for r in range(K)), Fraction(0))
        for i in range(K)
    ]
    k = [int((u[i] + half).__floor__()) for i in range(K)]
    u_frac = [u[i] - Fraction(k[i], 1) for i in range(K)]
    assert all(Fraction(-1, 2) <= val < Fraction(1, 2) for val in u_frac)
    z_babai = [
        int(z0[r] - sum(B_col[r][i] * k[i] for i in range(K))) for r in range(K)
    ]
    residual_e = [Fraction(z_babai[r], 1) - half for r in range(K)]
    return z_babai, residual_e, u_frac


def is_in_fundamental_parallelepiped(
    x: Sequence[int], B_col_inv_frac: Sequence[Sequence[Fraction]]
) -> bool:
    """Return True iff x in Z^K lies in c + B_col[-1/2, 1/2)^K."""
    K = len(x)
    half = Fraction(1, 2)
    shifted = [Fraction(int(x[r]), 1) - half for r in range(K)]
    for i in range(K):
        u_i = sum((B_col_inv_frac[i][r] * shifted[r] for r in range(K)), Fraction(0))
        if not (Fraction(-1, 2) <= u_i < Fraction(1, 2)):
            return False
    return True


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a concrete clean DCP Babai-rounding instance."""
    instance_id = str(instance["instance_id"])
    n = int(instance["n"])
    t = int(instance["t"])
    K = int(instance["K"])
    q = 1 << t
    delta = K - n * t
    A = [[int(x) for x in row] for row in instance["A"]]

    piv_cols, R_piv, B_col, B_col_inv_frac = build_qary_kernel_lll_basis(A, t)
    det_B = abs(int(fmpz_mat(B_col).det()))

    h = [0] * n
    h[0] = q // 2
    all_targets = list(itertools.product(range(q), repeat=n))

    babai_map: Dict[Tuple[int, ...], List[int]] = {}
    valid_targets: List[Tuple[int, ...]] = []
    overflow_targets: List[Tuple[int, ...]] = []
    coset_invariance_checks = 0
    half_integer_dichotomy_checks = 0
    max_linf_numerator = 1

    v_lat = [int(B_col[r][0]) for r in range(K)]

    for t_tuple in all_targets:
        z0 = [0] * K
        for i, c_p in enumerate(piv_cols):
            z0[c_p] = int(sum(R_piv[i][ell] * t_tuple[ell] for ell in range(n)) % q)

        z_babai, e_vec, _ = babai_round_exact(z0, B_col, B_col_inv_frac)
        z0_alt = [z0[r] + v_lat[r] for r in range(K)]
        z_babai_alt, _, _ = babai_round_exact(z0_alt, B_col, B_col_inv_frac)
        if z_babai == z_babai_alt:
            coset_invariance_checks += 1

        lhs = [
            int(sum(A[ell][r] * z_babai[r] for r in range(K)) % q)
            for ell in range(n)
        ]
        assert lhs == list(t_tuple)
        babai_map[t_tuple] = z_babai

        linf = max(abs(val) for val in e_vec)
        assert linf.denominator == 2 and linf.numerator % 2 == 1
        max_linf_numerator = max(max_linf_numerator, int(linf.numerator))
        in_boolean = all(x in (0, 1) for x in z_babai)
        if (in_boolean and linf == Fraction(1, 2)) or (
            (not in_boolean) and linf >= Fraction(3, 2)
        ):
            half_integer_dichotomy_checks += 1

        if in_boolean:
            valid_targets.append(t_tuple)
        else:
            overflow_targets.append(t_tuple)

    parallelepiped_boolean_vertices: List[Tuple[int, ...]] = []
    for x in itertools.product((0, 1), repeat=K):
        if is_in_fundamental_parallelepiped(x, B_col_inv_frac):
            parallelepiped_boolean_vertices.append(tuple(int(v) for v in x))

    babai_valid_witness_set = {tuple(babai_map[t_tup]) for t_tup in valid_targets}
    parallelepiped_vertex_set = set(parallelepiped_boolean_vertices)

    valid_target_set = set(valid_targets)
    paired_valid_targets = [
        t_tup
        for t_tup in valid_targets
        if tuple((t_tup[ell] + h[ell]) % q for ell in range(n)) in valid_target_set
    ]

    L = 1 << K
    f_map = [
        tuple(
            int(sum(A[ell][r] * ((x >> r) & 1) for r in range(K)) % q)
            for ell in range(n)
        )
        for x in range(L)
    ]
    swap_mutual_pairs = 0
    for x in range(L):
        t_x = tuple((f_map[x][ell] + h[ell]) % q for ell in range(n))
        w_tx = babai_map[t_x]
        if all(v in (0, 1) for v in w_tx):
            y = sum(int(w_tx[r]) << r for r in range(K))
            if f_map[y] == t_x:
                t_y = tuple((f_map[y][ell] + h[ell]) % q for ell in range(n))
                w_ty = babai_map[t_y]
                if all(v in (0, 1) for v in w_ty):
                    x_back = sum(int(w_ty[r]) << r for r in range(K))
                    if x_back == x:
                        swap_mutual_pairs += 1

    beta_babai = Fraction(len(valid_targets), q ** n)
    direct_filter_success = beta_babai * beta_babai * Fraction(1, 1 << delta)
    swap_adv_babai = Fraction(swap_mutual_pairs, 2 * L)
    expected_swap_adv = Fraction(len(paired_valid_targets), 2 * L)

    theorem1_passed = bool(
        det_B == (q ** n)
        and coset_invariance_checks == (q ** n)
        and len(babai_map) == (q ** n)
        and len(valid_targets) == len(parallelepiped_boolean_vertices)
        and babai_valid_witness_set == parallelepiped_vertex_set
    )
    theorem2_passed = bool(
        half_integer_dichotomy_checks == (q ** n)
        and len(valid_targets) + len(overflow_targets) == (q ** n)
    )
    theorem3_passed = bool(
        swap_adv_babai == expected_swap_adv
        and swap_mutual_pairs == len(paired_valid_targets)
    )

    return {
        "instance_id": instance_id,
        "n": int(n),
        "t": int(t),
        "q": int(q),
        "K": int(K),
        "A": A,
        "piv_cols": piv_cols,
        "R_piv": R_piv,
        "B_col": B_col,
        "lattice_determinant": int(det_B),
        "total_targets": int(q ** n),
        "coset_invariance_verified_targets": int(coset_invariance_checks),
        "valid_boolean_witness_targets": int(len(valid_targets)),
        "parallelepiped_boolean_vertex_count": int(
            len(parallelepiped_boolean_vertices)
        ),
        "box_overflow_target_count": int(len(overflow_targets)),
        "overflow_observed": bool(overflow_targets),
        "half_integer_dichotomy_verified_targets": int(half_integer_dichotomy_checks),
        "max_residual_linf_exact": f"{max_linf_numerator}/2",
        "verified_coverage_beta_babai_exact": str(beta_babai),
        "verified_coverage_beta_babai_float": float(beta_babai),
        "direct_filter_success_babai_exact": str(direct_filter_success),
        "paired_valid_targets_for_h": int(len(paired_valid_targets)),
        "swap_reciprocal_valid_pairs": int(swap_mutual_pairs),
        "forward_swap_advantage_babai_exact": str(swap_adv_babai),
        "forward_swap_advantage_babai_float": float(swap_adv_babai),
        "theorem1_coset_parallelepiped_identity_passed": bool(theorem1_passed),
        "theorem2_half_integer_dichotomy_passed": bool(theorem2_passed),
        "theorem3_babai_filter_swap_formula_passed": bool(theorem3_passed),
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def native_label_controls(
    *, bits_grid: Sequence[int] = (4, 8, 12, 16, 24, 32), n: int = 1,
    delta: int = 0, matrices_per_size: int = 4, target_samples: int = 128,
    seed: int = 20261016,
) -> Dict[str, Any]:
    """Test this public classical finder on unfiltered IID-label replay controls.

    Rank failures are retained as failures of this algorithm. Small target spaces
    are exhausted; larger ones use fixed-seed pseudo-random replay, NOT a claim
    of IID confidence. Independent target pairs estimate beta^2 without squaring
    a noisy estimate. This finite experiment is not an asymptotic no-go theorem.
    """
    if type(n) is not int or not 1 <= n <= 4:
        raise ValueError("native control components must be in [1,4]")
    if type(delta) is not int or not 0 <= delta <= 16:
        raise ValueError("delta must be in [0,16]")
    if type(matrices_per_size) is not int or not 1 <= matrices_per_size <= 64:
        raise ValueError("matrices_per_size must be in [1,64]")
    if type(target_samples) is not int or not 1 <= target_samples <= 4096:
        raise ValueError("target_samples must be in [1,4096]")
    if not bits_grid or any(type(t) is not int or not 2 <= t <= 64 or n*t+delta > 96
                            for t in bits_grid):
        raise ValueError("bounded native bit grid required")
    rng = random.Random(seed)
    rows = []
    for t in bits_grid:
        q, K = 1 << t, n*t + delta
        for matrix_index in range(matrices_per_size):
            A = [[rng.randrange(q) for _ in range(K)] for _ in range(n)]
            row = {"n": n, "phase_bits": t, "K": K, "delta": delta,
                   "matrix_index": matrix_index, "A": A,
                   "rank_failure_counted_as_zero_success": False}
            try:
                piv, inverse_pivot, B, inverse = build_qary_kernel_lll_basis(A, t)
            except ValueError:
                row.update({"rank_failure_counted_as_zero_success": True,
                            "coverage_fraction": "0", "paired_target_fraction": "0",
                            "direct_filter_success": "0", "forward_swap_advantage": "0",
                            "target_evaluation": "not_attempted_rank_failure", "finder_calls": 0})
                rows.append(row)
                continue
            determinant = q ** n
            scaled_inverse = [[v * determinant for v in inv_row] for inv_row in inverse]
            if any(v.denominator != 1 for inv_row in scaled_inverse for v in inv_row):
                raise ArithmeticError("integer adjugate invariant failed")
            adjugate = [[int(v) for v in inv_row] for inv_row in scaled_inverse]
            finder_calls = 0

            def valid(target):
                nonlocal finder_calls
                finder_calls += 1
                z0 = [0] * K
                for i, pivot in enumerate(piv):
                    z0[pivot] = sum(inverse_pivot[i][j] * target[j] for j in range(n)) % q
                twice_shifted = [2*v - 1 for v in z0]
                rounded = [(sum(a*b for a, b in zip(inv_row, twice_shifted)) + determinant)
                           // (2*determinant) for inv_row in adjugate]
                witness = [z0[r] - sum(B[r][j] * rounded[j] for j in range(K)) for r in range(K)]
                if any(v not in (0, 1) for v in witness):
                    return False
                if any(sum(A[i][j] * witness[j] for j in range(K)) % q != target[i]
                       for i in range(n)):
                    raise ArithmeticError("purported witness fails public equation")
                return True

            if determinant <= 256:
                valid_set = {target for target in itertools.product(range(q), repeat=n) if valid(target)}
                beta = Fraction(len(valid_set), determinant)
                paired = Fraction(sum(((target[0]+q//2) % q, *target[1:]) in valid_set
                                      for target in valid_set), determinant)
                direct = beta * beta / (1 << delta)
                mode = "exhaustive_targets_exact_conditional_on_this_matrix"
            else:
                successes = paired_successes = independent_successes = 0
                for _ in range(target_samples):
                    target = tuple(rng.randrange(q) for _ in range(n))
                    independent_target = tuple(rng.randrange(q) for _ in range(n))
                    a = valid(target)
                    b = valid(((target[0]+q//2) % q, *target[1:]))
                    c = valid(independent_target)
                    successes += a
                    paired_successes += a and b
                    independent_successes += a and c
                beta = Fraction(successes, target_samples)
                paired = Fraction(paired_successes, target_samples)
                direct = Fraction(independent_successes, target_samples * (1 << delta))
                mode = "pseudo_random_target_replay_not_confidence_certificate"
            row.update({"coverage_fraction": str(beta), "paired_target_fraction": str(paired),
                        "direct_filter_success": str(direct),
                        "forward_swap_advantage": str(paired / (2 << delta)),
                        "target_evaluation": mode, "finder_calls": finder_calls})
            rows.append(row)
    return {"schema_version": "1.0", "subsystem": "dcp_coordinate_rounding_native_controls",
            "seed": seed, "label_selection": "unfiltered_pseudo_random_IID_uniform_replay",
            "uniform_secret_unknown_to_finder": True,
            "matrices_per_size": matrices_per_size, "target_samples_when_not_exhaustive": target_samples,
            "rows": rows, "source_qubits_per_attempt": "K ORIGINAL phase qubits",
            "quantum_circuit_compiled": False, "asymptotic_advantage_or_decay_proved": False,
            "fixed_seed_is_not_IID_confidence_certificate": True,
            "reported_rates_are_replay_frequencies_not_performance_guarantees": True,
            "no_source_matrix_conditioning_or_discarded_rank_failures": True,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "inverse_dependency_sha256": hashlib.sha256(
                (ROOT/"theorems/dcp_clean_linear_witness_carry_obstruction.py").read_bytes()).hexdigest()}


def build_dcp_babai_lattice_rounding_witness_obstruction_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]

    all_t1 = bool(
        all(inst["theorem1_coset_parallelepiped_identity_passed"] for inst in instances)
    )
    all_t2 = bool(
        all(inst["theorem2_half_integer_dichotomy_passed"] for inst in instances)
    )
    all_t3 = bool(
        all(inst["theorem3_babai_filter_swap_formula_passed"] for inst in instances)
    )
    all_passed = bool(all_t1 and all_t2 and all_t3)

    min_beta = float(
        min(inst["verified_coverage_beta_babai_float"] for inst in instances)
    )
    min_swap_adv = float(
        min(inst["forward_swap_advantage_babai_float"] for inst in instances)
    )

    payload_for_hash = {
        "contract_id": contract["contract_id"],
        "instances": instances,
        "all_passed": all_passed,
    }
    digest = hashlib.sha256(
        json.dumps(payload_for_hash, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "2.0",
        "subsystem": "dcp_babai_lattice_rounding_witness_obstruction",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_BABAI_LATTICE_ROUNDING_WITNESS_OBSTRUCTION.md",
        "contract_path": "research/hypotheses/dcp_babai_lattice_rounding_witness_obstruction_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_coset_parallelepiped_identity_passed": bool(all_t1),
            "theorem2_half_integer_dichotomy_passed": bool(all_t2),
            "theorem3_babai_filter_swap_formula_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "universal_overflow_claim": "RETRACTED_BY_STRUCTURED_COUNTEREXAMPLE",
            "general_decay_bound_proved": False,
            "verification_scope": "finite_identity_controls_and_local_derivations_review_pending",
            "min_verified_coverage_beta_float": float(min_beta),
            "min_forward_swap_advantage_float": float(min_swap_adv),
        },
        "instances": instances,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
            "rounding_method": "basis_coordinate_rounding_not_nearest_plane",
            "finite_calibration_not_a_uniform_source_scaling_theorem": True,
        },
        "sha256": str(digest),
    }


def write_dcp_babai_lattice_rounding_witness_obstruction_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_babai_lattice_rounding_witness_obstruction_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the clean DCP LLL/Babai lattice-rounding witness obstruction audit."
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
    parser.add_argument("--native-controls", action="store_true",
                        help="Run finite unfiltered native-label coordinate-rounding controls.")
    args = parser.parse_args()

    if args.native_controls:
        report = native_label_controls()
        if args.write:
            artifact = ROOT/"research/phase_workbench/dcp_coordinate_rounding_native_controls.json"
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            for row in report["rows"]:
                print(f"bits={row['phase_bits']} K={row['K']} matrix={row['matrix_index']} "
                      f"coverage={row['coverage_fraction']} direct={row['direct_filter_success']} "
                      f"parity_adv={row['forward_swap_advantage']} mode={row['target_evaluation']}")
        return 0

    if args.write:
        report = write_dcp_babai_lattice_rounding_witness_obstruction_report()
    else:
        report = build_dcp_babai_lattice_rounding_witness_obstruction_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_babai_lattice_rounding_witness_obstruction] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"min_beta={s['min_verified_coverage_beta_float']:.4f} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
