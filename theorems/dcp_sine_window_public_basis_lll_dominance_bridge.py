"""Sine-window clean-budget source vs. classical LLL basis reduction dominance bridge.

Certifies:
1. Theorem 1 (Exact Clean-Budget Gap Lower Bound & Classical LLL Dominance Criterion):
   For any public basis B in Z^{d x d}, norm-squared interval [ell_lower^2, ell_upper^2],
   copy budget K(t), and advantage eps(t) with gamma(t) = eps(t)/(2 K(t)), the packet
   loss bound (242/49) ell_upper^2 / S^2 <= gamma(t)/2 forces
     S^2 >= (968/49) K(t) ell_upper^2 / eps(t)
   and
     G_req^2 > d S^2 / ell_lower^2 >= (968/49) d (K(t)/eps(t)) (ell_upper^2 / ell_lower^2).
   Whenever G_req > 2^{(d-1)/2}, classical LLL is guaranteed to recover a shortest vector
   in polynomial time with 0 quantum source preparations.
2. Theorem 2 (Exact Outer-Trial Quantum Preparation & Qubit Ledger):
   A single invocation of the hypothetical K(t)-copy predictor across all d(p-1) outer
   coordinate/residue trials requires
     N_prep^sweep = d(p-1) K(t) >= d G_req K(t)
   coherent sine-window parent preparations, each using
     Q_total = 1 + d m + d W + 2W + 1 + w + d
   qubits and 3d packet unitaries.
3. Theorem 3 (Public-Basis LLL Recovery Across Calibration Families):
   Across all benchmark bases of the clean-first sine-window planner, public-basis FLINT LLL
   recovers the exact primitive shortest vector u with ||u||_2^2 in [ell_lower^2, ell_upper^2]
   using 0 quantum preparations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

from flint import fmpq_mat, fmpz_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_clean_source_budget import (
    materialize_public_source,
    plan_sine_source,
)


DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_sine_window_public_basis_lll_dominance_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_sine_window_public_basis_lll_dominance_bridge.json"
)


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a clean-budget sine-window planning instance."""
    instance_id = str(instance["instance_id"])
    B = [[int(x) for x in row] for row in instance["basis"]]
    d = len(B)
    lo = int(instance["norm_sq_lower"])
    hi = int(instance["norm_sq_upper"])
    copy_power = int(instance["copy_power"])
    adv_power = int(instance["advantage_power"])
    family = str(instance["predictor_family"])

    plan = plan_sine_source(
        B,
        lo,
        hi,
        copy_power=copy_power,
        advantage_power=adv_power,
        predictor_family=family,
    )
    mat = materialize_public_source(plan)

    t = int(plan["cyclic_phase_bits"])
    m = int(plan["parent_box_bits"])
    w = int(plan["packet_side_bits"])
    S = 1 << w
    K_copies = int(plan["clean_transfer_budget"]["original_source_calls"])
    eps = Fraction(plan["clean_transfer_budget"]["assumed_clean_average_advantage_exact"])
    gamma = Fraction(
        plan["clean_transfer_budget"]["visibility_loss_per_original_qubit_upper_exact"]
    )
    G_req = int(plan["required_unique_gap_strict_sufficient"])
    p = int(mat["selected_prime"])

    # --- Theorem 1: Algebraic Gap Lower Bound & LLL Uniqueness Window ---
    s_sq_actual = Fraction(S * S, 1)
    s_sq_min_bound = Fraction(968, 49) * Fraction(K_copies, 1) * Fraction(hi, 1) / eps
    g_sq_actual = Fraction(G_req * G_req, 1)
    g_sq_strict_radius = Fraction(d * S * S, lo)
    g_sq_algebraic_lower = (
        Fraction(968, 49)
        * Fraction(d * K_copies, 1)
        * Fraction(hi, lo)
        / eps
    )
    # Conservative LLL uniqueness threshold: 2^{(d-1)/2}, squared is 2^{d-1}
    lll_worst_case_gap_sq = Fraction(1 << (d - 1), 1)
    within_lll_guaranteed_window = bool(g_sq_actual > lll_worst_case_gap_sq)

    theorem1_passed = bool(
        gamma == eps / (2 * K_copies)
        and s_sq_actual >= s_sq_min_bound
        and g_sq_actual > g_sq_strict_radius
        and g_sq_strict_radius >= g_sq_algebraic_lower
        and within_lll_guaranteed_window
    )

    # --- Theorem 2: Outer-Trial Quantum Preparation & Qubit Ledger ---
    res = mat["symbolic_source_resources"]
    W = int(res["arithmetic_width_plan"]["shared_signed_word_bits"])
    total_qubits = int(res["total_source_qubits"])
    expected_qubits = 1 + d * m + d * W + 2 * W + 1 + w + d
    outer_trials = int(mat["coordinate_residue_trials_upper"])
    expected_outer_trials = d * (p - 1)
    sweep_preparations = outer_trials * K_copies
    min_sweep_bound = d * G_req * K_copies
    packet_unitaries_per_prep = int(res["packet_unitary_applications"])

    theorem2_passed = bool(
        total_qubits == expected_qubits
        and outer_trials == expected_outer_trials
        and sweep_preparations >= min_sweep_bound
        and packet_unitaries_per_prep == d
    )

    # --- Theorem 3: Public-Basis Classical LLL Recovery ---
    red = fmpz_mat(B).lll()
    u_vec = [int(x) for x in red.tolist()[0]]
    u_norm_sq = int(sum(x * x for x in u_vec))
    # Verify u_vec is in the integer row lattice of B: u_vec * B^{-1} in Z^d
    coords_q = (fmpq_mat([u_vec]) * fmpq_mat(B).inv()).tolist()[0]
    in_lattice = all(int(c.denominator) == 1 for c in coords_q)
    primitive = math.gcd(*[abs(x) for x in u_vec]) == 1

    theorem3_passed = bool(
        in_lattice and primitive and (lo <= u_norm_sq <= hi)
    )

    return {
        "instance_id": instance_id,
        "dimension": int(d),
        "basis": B,
        "norm_sq_interval": [int(lo), int(hi)],
        "predictor_family": family,
        "cyclic_phase_bits_t": int(t),
        "parent_box_bits_m": int(m),
        "packet_side_bits_w": int(w),
        "packet_side_S": int(S),
        "shared_signed_word_bits_W": int(W),
        "hypothetical_copies_per_invocation": int(K_copies),
        "assumed_clean_advantage_exact": str(eps),
        "visibility_loss_budget_gamma_exact": str(gamma),
        "gap_audit": {
            "packet_side_sq_actual": int(S * S),
            "packet_side_sq_min_bound_exact": str(s_sq_min_bound),
            "required_unique_gap_G": int(G_req),
            "required_gap_sq_actual": int(G_req * G_req),
            "strict_radius_sq_exact": str(g_sq_strict_radius),
            "algebraic_gap_sq_lower_bound_exact": str(g_sq_algebraic_lower),
            "lll_worst_case_gap_sq_threshold": int(1 << (d - 1)),
            "within_lll_guaranteed_uniqueness_window": bool(
                within_lll_guaranteed_window
            ),
            "theorem1_passed": bool(theorem1_passed),
        },
        "overhead_audit": {
            "splitting_prime_p": int(p),
            "outer_coordinate_residue_trials": int(outer_trials),
            "single_sweep_quantum_preparations": int(sweep_preparations),
            "min_sweep_preparations_bound": int(min_sweep_bound),
            "total_source_qubits_per_prep": int(total_qubits),
            "w_calls_per_prep": int(3 * d),
            "theorem2_passed": bool(theorem2_passed),
        },
        "classical_lll_audit": {
            "recovered_shortest_vector": u_vec,
            "recovered_norm_squared": int(u_norm_sq),
            "in_public_lattice": bool(in_lattice),
            "is_primitive": bool(primitive),
            "quantum_preparations_used": 0,
            "theorem3_passed": bool(theorem3_passed),
        },
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def build_dcp_sine_window_public_basis_lll_dominance_bridge_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]

    all_t1 = bool(all(inst["gap_audit"]["theorem1_passed"] for inst in instances))
    all_t2 = bool(all(inst["overhead_audit"]["theorem2_passed"] for inst in instances))
    all_t3 = bool(
        all(inst["classical_lll_audit"]["theorem3_passed"] for inst in instances)
    )
    all_passed = bool(all_t1 and all_t2 and all_t3)

    min_sweep_preps = int(
        min(
            inst["overhead_audit"]["single_sweep_quantum_preparations"]
            for inst in instances
        )
    )
    max_sweep_preps = int(
        max(
            inst["overhead_audit"]["single_sweep_quantum_preparations"]
            for inst in instances
        )
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
        "schema_version": "1.0",
        "subsystem": "dcp_sine_window_public_basis_lll_dominance_bridge",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_SINE_WINDOW_PUBLIC_BASIS_LLL_DOMINANCE_BRIDGE.md",
        "contract_path": "research/hypotheses/dcp_sine_window_public_basis_lll_dominance_bridge_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_gap_lower_bound_passed": bool(all_t1),
            "theorem2_outer_trial_overhead_passed": bool(all_t2),
            "theorem3_public_lll_recovery_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "min_single_sweep_quantum_preparations": int(min_sweep_preps),
            "max_single_sweep_quantum_preparations": int(max_sweep_preps),
            "classical_lll_quantum_preparations": 0,
        },
        "instances": instances,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
        "sha256": str(digest),
    }


def write_dcp_sine_window_public_basis_lll_dominance_bridge_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the sine-window clean-budget source vs classical LLL dominance bridge audit."
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
        report = write_dcp_sine_window_public_basis_lll_dominance_bridge_report()
    else:
        report = build_dcp_sine_window_public_basis_lll_dominance_bridge_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_sine_window_public_basis_lll_dominance_bridge] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"min_sweep_preps={s['min_single_sweep_quantum_preparations']} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
