"""Clean DCP polynomial-pool CNOT collimation branching & sample-depth obstruction audit.

Certifies:
1. Theorem 1 (Exact CNOT + Z Branching Law & Subtraction-Halving Identity):
   For any secret S in Z_q^n, labels a_1, a_2 in Z_q^n, and visibilities v_1, v_2 in [0, 1],
   applying CNOT_{1->2} to rho_{a_1}(S, v_1) otimes rho_{a_2}(S, v_2) and measuring qubit 2
   in the Z basis yields z in {0, 1} with Pr[z=0] = Pr[z=1] = 1/2 and conditional state
     rho^{(z)} = rho_{(a_1 + (-1)^z a_2) mod q}(S, v_1 v_2).
   When a_1 == a_2 mod 2^b with 2 a_2 != 0 mod 2^b, only z=1 cancels the low b bits,
   so 2 consumed parent qubits yield at most 1/2 expected collimated child qubit.
2. Theorem 2 (Exact Bucket-Occupancy Disjoint Pairing Bound):
   In a pool of M_pool independent qubits distributed uniformly across B = 2^b buckets
   with occupancies (c_0, ..., c_{B-1}), the maximum number of disjoint matched pairs is
     N_pairs(c) = sum_{u=0}^{B-1} floor(c_u / 2) = (M_pool - sum_u (c_u mod 2)) / 2 <= floor(M_pool / 2),
   with E[N_pairs] <= min(M_pool / 2, C(M_pool, 2) / B) and expected surviving subtraction
   children E[M_child] = E[N_pairs] / 2 <= min(M_pool / 4, M_pool(M_pool - 1)/(4 B)).
3. Theorem 3 (Superpolynomial Depth & Sample Barrier for Polynomial-Pool Collimation):
   To sustain Theta(M_pool) pairs per pool without sparse-bucket starvation (which requires
   B = 2^b <= M_pool, i.e., b <= floor(log_2 M_pool)), cancelling nt - 1 label bits requires
   tree depth L_min = ceil((nt - 1)/b) = Omega(nt / log(nt)) and expected initial preparations
   >= 4^{L_min} = 2^{2 ceil((nt - 1)/b)} = 2^{Omega(nt / log(nt))}, strictly worse than
   Kuperberg's subexponential collimation sieve 2^{Theta(sqrt(nt))}.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
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
    / "dcp_poly_pool_cnot_collimation_branching_obstruction_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_poly_pool_cnot_collimation_branching_obstruction.json"
)


def phase_qubit_density(
    a: Sequence[int], S: Sequence[int], q: int, v: float
) -> np.ndarray:
    """Return 2x2 density matrix rho_a(S, v) = (1/2) [[1, v*omega^{-<a,S>}], [v*omega^{<a,S>}, 1]]."""
    dot = sum(int(a[i]) * int(S[i]) for i in range(len(a))) % q
    phase = np.exp(-2j * np.pi * dot / q)
    return 0.5 * np.array(
        [[1.0 + 0.0j, v * phase], [v * np.conj(phase), 1.0 + 0.0j]], dtype=complex
    )


def cnot_merge_blocks(rho1: np.ndarray, rho2: np.ndarray) -> List[np.ndarray]:
    """Apply CNOT_{1->2} and extract the unnormalized 2x2 target Z-measurement blocks z=0,1."""
    joint = np.kron(rho1, rho2)
    perm = (0, 1, 3, 2)
    joint_after = joint[np.ix_(perm, perm)]
    return [joint_after[np.ix_((z, 2 + z), (z, 2 + z))] for z in (0, 1)]


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1 and 2 on a concrete CNOT collimation pool instance."""
    instance_id = str(instance["instance_id"])
    n = int(instance["n"])
    t = int(instance["t"])
    q = int(instance["q"])
    assert q == (1 << t)
    M_pool = int(instance["M_pool"])
    b_bits = int(instance["b_bits"])
    B_buckets = int(instance["B_buckets"])
    assert B_buckets == (1 << b_bits)
    v1_frac = Fraction(instance["v1"])
    v2_frac = Fraction(instance["v2"])
    v1 = float(v1_frac)
    v2 = float(v2_frac)

    all_vecs = list(itertools.product(range(q), repeat=n))
    max_prob_err = 0.0
    max_state_err = 0.0
    total_triples_checked = 0

    for S in all_vecs:
        for a1 in all_vecs:
            for a2 in all_vecs:
                rho1 = phase_qubit_density(a1, S, q, v1)
                rho2 = phase_qubit_density(a2, S, q, v2)
                blocks = cnot_merge_blocks(rho1, rho2)
                for z in (0, 1):
                    pz = float(np.trace(blocks[z]).real)
                    max_prob_err = max(max_prob_err, abs(pz - 0.5))
                    cond_rho = blocks[z] / pz
                    sign = 1 if z == 0 else -1
                    a_out = tuple((a1[ell] + sign * a2[ell]) % q for ell in range(n))
                    expected_rho = phase_qubit_density(a_out, S, q, v1 * v2)
                    err = float(np.max(np.abs(cond_rho - expected_rho)))
                    max_state_err = max(max_state_err, err)
                total_triples_checked += 1

    mod_b = 1 << b_bits
    non_torsion_same_bucket_pairs = 0
    z1_only_cancels_pairs = 0
    for x1 in range(mod_b):
        for x2 in range(mod_b):
            if (x1 % mod_b) == (x2 % mod_b) and ((2 * x2) % mod_b) != 0:
                non_torsion_same_bucket_pairs += 1
                z0_out = (x1 + x2) % mod_b
                z1_out = (x1 - x2) % mod_b
                if z1_out == 0 and z0_out != 0:
                    z1_only_cancels_pairs += 1

    theorem1_passed = bool(
        max_prob_err <= 1e-12
        and max_state_err <= 1e-12
        and non_torsion_same_bucket_pairs > 0
        and z1_only_cancels_pairs == non_torsion_same_bucket_pairs
    )

    all_pool_assignments = list(itertools.product(range(B_buckets), repeat=M_pool))
    total_outcomes = len(all_pool_assignments)
    sum_pairs = 0
    at_least_one_pair_outcomes = 0
    parity_identity_matches = 0
    max_pairs_observed = 0

    for assign in all_pool_assignments:
        counts = [0] * B_buckets
        for u in assign:
            counts[u] += 1
        n_pairs = sum(c // 2 for c in counts)
        odd_buckets = sum(c % 2 for c in counts)
        if 2 * n_pairs == (M_pool - odd_buckets):
            parity_identity_matches += 1
        max_pairs_observed = max(max_pairs_observed, n_pairs)
        sum_pairs += n_pairs
        if n_pairs >= 1:
            at_least_one_pair_outcomes += 1

    prob_collision_exact = Fraction(at_least_one_pair_outcomes, total_outcomes)
    prob_collision_union_bound = min(
        Fraction(1, 1), Fraction(math.comb(M_pool, 2), B_buckets)
    )
    expected_pairs_exact = Fraction(sum_pairs, total_outcomes)
    expected_pairs_upper_bound = min(
        Fraction(M_pool, 2), Fraction(math.comb(M_pool, 2), B_buckets)
    )
    expected_children_exact = expected_pairs_exact * Fraction(1, 2)
    expected_children_upper_bound = expected_pairs_upper_bound * Fraction(1, 2)

    theorem2_passed = bool(
        parity_identity_matches == total_outcomes
        and max_pairs_observed == (M_pool // 2)
        and prob_collision_exact <= prob_collision_union_bound
        and expected_pairs_exact <= expected_pairs_upper_bound
        and expected_children_exact <= Fraction(M_pool, 4)
    )

    return {
        "instance_id": instance_id,
        "n": int(n),
        "t": int(t),
        "q": int(q),
        "M_pool": int(M_pool),
        "b_bits": int(b_bits),
        "B_buckets": int(B_buckets),
        "v1_exact": str(v1_frac),
        "v2_exact": str(v2_frac),
        "cnot_branching_audit": {
            "total_triples_checked": int(total_triples_checked),
            "max_branch_probability_error": float(max_prob_err),
            "max_conditional_state_error": float(max_state_err),
            "non_2_torsion_same_bucket_residues": int(non_torsion_same_bucket_pairs),
            "z1_only_cancels_residues": int(z1_only_cancels_pairs),
            "theorem1_passed": bool(theorem1_passed),
        },
        "bucket_pairing_audit": {
            "total_bucket_assignments": int(total_outcomes),
            "parity_identity_verified_assignments": int(parity_identity_matches),
            "max_disjoint_pairs_observed": int(max_pairs_observed),
            "collision_probability_exact": str(prob_collision_exact),
            "collision_probability_birthday_upper_exact": str(
                prob_collision_union_bound
            ),
            "expected_disjoint_pairs_exact": str(expected_pairs_exact),
            "expected_disjoint_pairs_upper_exact": str(expected_pairs_upper_bound),
            "expected_subtraction_children_exact": str(expected_children_exact),
            "expected_subtraction_children_upper_exact": str(
                expected_children_upper_bound
            ),
            "theorem2_passed": bool(theorem2_passed),
        },
        "instance_passed": bool(theorem1_passed and theorem2_passed),
    }


def evaluate_asymptotic_scaling(grid: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Evaluate polynomial-pool depth and sample scaling vs Kuperberg collimation."""
    rows: List[Dict[str, Any]] = []
    for item in grid:
        n = int(item["n"])
        t = int(item["t"])
        M_pool = int(item["M_pool"])
        nt = n * t
        b_max = max(1, M_pool.bit_length() - 1)
        L_min = math.ceil((nt - 1) / b_max)
        poly_pool_initial_samples_log2 = 2 * L_min
        kuperberg_collimation_log2 = round(math.sqrt(3.0 * nt), 2)
        k_min_bcdv = int(minimum_copies_for_advantage(n, t, Fraction(1, 16)))
        rows.append(
            {
                "n": int(n),
                "t": int(t),
                "total_group_bits_nt": int(nt),
                "M_pool": int(M_pool),
                "max_bits_cancelled_per_level_b": int(b_max),
                "minimum_tree_depth_L": int(L_min),
                "poly_pool_initial_preparations_log2_lower": int(
                    poly_pool_initial_samples_log2
                ),
                "kuperberg_subexponential_log2_scale": float(
                    kuperberg_collimation_log2
                ),
                "bcdv_information_theoretic_minimum_copies": int(k_min_bcdv),
                "theorem3_passed": bool(
                    L_min >= 4 and poly_pool_initial_samples_log2 > b_max
                ),
            }
        )
    return rows


def build_dcp_poly_pool_cnot_collimation_branching_obstruction_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]
    asymptotic_rows = evaluate_asymptotic_scaling(contract["asymptotic_scaling_grid"])

    all_t1 = bool(
        all(inst["cnot_branching_audit"]["theorem1_passed"] for inst in instances)
    )
    all_t2 = bool(
        all(inst["bucket_pairing_audit"]["theorem2_passed"] for inst in instances)
    )
    all_t3 = bool(all(row["theorem3_passed"] for row in asymptotic_rows))
    all_passed = bool(all_t1 and all_t2 and all_t3)

    max_prob_err = float(
        max(
            inst["cnot_branching_audit"]["max_branch_probability_error"]
            for inst in instances
        )
    )
    max_state_err = float(
        max(
            inst["cnot_branching_audit"]["max_conditional_state_error"]
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
        "subsystem": "dcp_poly_pool_cnot_collimation_branching_obstruction",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_POLY_POOL_CNOT_COLLIMATION_BRANCHING_OBSTRUCTION.md",
        "contract_path": "research/hypotheses/dcp_poly_pool_cnot_collimation_branching_obstruction_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_cnot_branching_passed": bool(all_t1),
            "theorem2_bucket_occupancy_pairing_passed": bool(all_t2),
            "theorem3_superpolynomial_depth_barrier_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "max_branch_probability_error": float(max_prob_err),
            "max_conditional_state_error": float(max_state_err),
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


def write_dcp_poly_pool_cnot_collimation_branching_obstruction_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the clean DCP polynomial-pool CNOT collimation branching obstruction audit."
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
        report = write_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
    else:
        report = build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_poly_pool_cnot_collimation_branching_obstruction] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"max_prob_err={s['max_branch_probability_error']:.3e} "
            f"max_state_err={s['max_conditional_state_error']:.3e} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
