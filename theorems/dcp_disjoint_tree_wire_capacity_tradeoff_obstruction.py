"""Disjoint-block coherent 2^a-tree receiver wire-capacity & list-width AM-GM tradeoff audit.

Certifies:
1. Theorem 1 (Exact Physical-Wire Capacity Inequality for Disjoint-Block 2^a-Trees):
   In any disjoint-block 2^a-tree over an N_bits-bit group where each of the k = 2^a
   leaves supplies L_list = 2^{b_bits} (b_bits = ceil(N_bits / (a + 1))) distinct
   non-empty supports inside its dedicated m_leaf-wire block, C(m_leaf, floor(m_leaf / 2)) >= 2^{b_bits}
   forces m_leaf >= m_leaf^min(b_bits) >= b_bits + 1 and total physical phase-qubit width
     K_wires(a, N_bits) >= 2^a * m_leaf^min(b_bits) >= 2^a * (b_bits + 1).
2. Theorem 2 (Polynomial-Wire Depth Ceiling & Oblivious-Join Lower Bound):
   Under any phase-qubit budget K >= 2, every feasible disjoint-block tree depth
   a in A(K, N_bits) = {a >= 0 : 2^a * m_leaf^min(ceil(N_bits / (a + 1))) <= K}
   satisfies a <= floor(log_2 K), and the minimum oblivious-join record-complexity
   exponent satisfies
     E_obliv^min(K, N_bits) = min_{a in A(K, N_bits)} (a + ceil(N_bits / (a + 1)))
                            >= ceil(N_bits / (floor(log_2 K) + 1)).
3. Theorem 3 (Unconstrained AM-GM Joint List-Width Frontier):
   Across all unconstrained integer tree depths a >= 0, the oblivious-join record
   exponent E(a, N_bits) = a + ceil(N_bits / (a + 1)) satisfies
     E(a, N_bits) >= ceil(2 * sqrt(N_bits)) - 1,
   attained at a* in {max(0, floor(sqrt(N_bits)) - 1), ceil(sqrt(N_bits)) - 1},
   where required physical wire width is K_wires(a*, N_bits) = 2^{Theta(sqrt(N_bits))}.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.json"
)


def min_leaf_wires_for_list_exponent(b_bits: int) -> int:
    """Return least m >= 1 such that C(m, floor(m/2)) >= 2^{b_bits}."""
    target = 1 << int(b_bits)
    m = max(1, int(b_bits) + 1)
    while math.comb(m, m // 2) < target:
        m += 1
    assert math.comb(m - 1, (m - 1) // 2) < target
    return int(m)


def min_support_weight(m_leaf: int, b_bits: int) -> int:
    """Return least w in {1, ..., m_leaf} such that C(m_leaf, w) >= 2^{b_bits}."""
    target = 1 << int(b_bits)
    for w in range(1, m_leaf + 1):
        if math.comb(m_leaf, w) >= target:
            return int(w)
    raise ValueError("m_leaf insufficient for 2^{b_bits} supports")


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a disjoint-block tree frontier instance."""
    instance_id = str(instance["instance_id"])
    N_bits = int(instance["N_bits"])
    K_budget = int(instance["K_budget"])
    v_frac = Fraction(instance["visibility"])
    max_depth = int(instance["max_depth_sweep"])

    depth_records: List[Dict[str, Any]] = []
    feasible_depths: List[int] = []
    feasible_obliv_exponents: List[int] = []
    feasible_cartesian_exponents: List[int] = []
    am_gm_lower_bound = math.ceil(2.0 * math.sqrt(float(N_bits))) - 1

    theorem1_all_depths_ok = True
    theorem3_all_depths_ok = True

    for a in range(max_depth + 1):
        k_leaves = 1 << a
        b_bits = math.ceil(N_bits / (a + 1))
        m_leaf_min = min_leaf_wires_for_list_exponent(b_bits)
        w_min = min_support_weight(m_leaf_min, b_bits)
        K_wires_min = k_leaves * m_leaf_min
        root_mask_weight = k_leaves * w_min
        obliv_exp = a + b_bits
        cartesian_exp = a + 2 * b_bits
        feasible = bool(K_wires_min <= K_budget)

        if not (m_leaf_min >= b_bits + 1 and K_wires_min >= k_leaves * (b_bits + 1)):
            theorem1_all_depths_ok = False
        if not (obliv_exp >= am_gm_lower_bound):
            theorem3_all_depths_ok = False

        if feasible:
            feasible_depths.append(int(a))
            feasible_obliv_exponents.append(int(obliv_exp))
            feasible_cartesian_exponents.append(int(cartesian_exp))

        depth_records.append(
            {
                "a": int(a),
                "k_leaves": int(k_leaves),
                "b_bits_per_level": int(b_bits),
                "m_leaf_min": int(m_leaf_min),
                "w_support_min": int(w_min),
                "K_wires_min": int(K_wires_min),
                "root_mask_weight": int(root_mask_weight),
                "oblivious_join_record_exponent": int(obliv_exp),
                "cartesian_join_record_exponent": int(cartesian_exp),
                "feasible_under_K_budget": bool(feasible),
            }
        )

    log2_K_floor = K_budget.bit_length() - 1
    max_feasible_a = max(feasible_depths)
    min_feasible_obliv_exp = min(feasible_obliv_exponents)
    min_feasible_cartesian_exp = min(feasible_cartesian_exponents)
    theoretical_obliv_lower_under_K = math.ceil(N_bits / (log2_K_floor + 1))

    # Theorem 3: Exact unconstrained AM-GM optimum at a* in {floor(sqrt(N))-1, ceil(sqrt(N))-1}
    a_floor = max(0, math.isqrt(N_bits) - 1)
    a_ceil = max(0, math.ceil(math.sqrt(float(N_bits))) - 1)
    cand_exps = {
        a_cand: a_cand + math.ceil(N_bits / (a_cand + 1))
        for a_cand in (a_floor, a_ceil)
    }
    a_star = min(cand_exps, key=cand_exps.get)
    e_star = cand_exps[a_star]
    b_star = math.ceil(N_bits / (a_star + 1))
    m_star = min_leaf_wires_for_list_exponent(b_star)
    K_wires_at_a_star = (1 << a_star) * m_star

    # Verify global minimum across all a in 0..N_bits equals e_star
    global_min_exp = min(a + math.ceil(N_bits / (a + 1)) for a in range(N_bits + 1))

    theorem1_passed = bool(theorem1_all_depths_ok and len(feasible_depths) >= 1)
    theorem2_passed = bool(
        max_feasible_a <= log2_K_floor
        and min_feasible_obliv_exp >= theoretical_obliv_lower_under_K
        and min_feasible_cartesian_exp > min_feasible_obliv_exp
    )
    theorem3_passed = bool(
        theorem3_all_depths_ok
        and e_star == global_min_exp
        and e_star == am_gm_lower_bound
    )

    return {
        "instance_id": instance_id,
        "N_bits": int(N_bits),
        "K_budget": int(K_budget),
        "visibility_exact": str(v_frac),
        "log2_K_floor": int(log2_K_floor),
        "feasible_depths": feasible_depths,
        "max_feasible_depth_a": int(max_feasible_a),
        "min_feasible_oblivious_record_exponent": int(min_feasible_obliv_exp),
        "min_feasible_cartesian_record_exponent": int(min_feasible_cartesian_exp),
        "theoretical_wire_constrained_oblivious_lower_exponent": int(
            theoretical_obliv_lower_under_K
        ),
        "unconstrained_am_gm_optimum": {
            "a_star": int(a_star),
            "b_star": int(b_star),
            "m_leaf_min_at_a_star": int(m_star),
            "K_wires_required_at_a_star": int(K_wires_at_a_star),
            "optimal_oblivious_record_exponent": int(e_star),
            "am_gm_lower_bound_exponent": int(am_gm_lower_bound),
            "exceeds_K_budget": bool(K_wires_at_a_star > K_budget),
        },
        "depth_sweep": depth_records,
        "theorem1_wire_capacity_passed": bool(theorem1_passed),
        "theorem2_depth_ceiling_passed": bool(theorem2_passed),
        "theorem3_am_gm_frontier_passed": bool(theorem3_passed),
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]

    all_t1 = bool(all(inst["theorem1_wire_capacity_passed"] for inst in instances))
    all_t2 = bool(all(inst["theorem2_depth_ceiling_passed"] for inst in instances))
    all_t3 = bool(all(inst["theorem3_am_gm_frontier_passed"] for inst in instances))
    all_passed = bool(all_t1 and all_t2 and all_t3)

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
        "subsystem": "dcp_disjoint_tree_wire_capacity_tradeoff_obstruction",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_DISJOINT_TREE_WIRE_CAPACITY_TRADEOFF_OBSTRUCTION.md",
        "contract_path": "research/hypotheses/dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_wire_capacity_passed": bool(all_t1),
            "theorem2_depth_ceiling_passed": bool(all_t2),
            "theorem3_am_gm_frontier_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
        },
        "instances": instances,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
        "sha256": str(digest),
    }


def write_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the disjoint-block coherent 2^a-tree wire-capacity tradeoff obstruction audit."
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
        report = write_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    else:
        report = build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_disjoint_tree_wire_capacity_tradeoff_obstruction] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
