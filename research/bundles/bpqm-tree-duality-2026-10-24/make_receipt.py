"""Replay the existing quantum bounds and certify the paired classical basin."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import tree_duality as t

HERE = Path(__file__).resolve().parent


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2)+"\n").encode("ascii")


def report():
    reference = json.loads((HERE/"reference_frontier.json").read_text())
    result = t.bounded_tree()
    replay = [row["mean_quantum_overlap_upper"] for row in result["history"][:12]]
    if replay != reference["upper_fidelity_history"]:
        raise ArithmeticError("original quantum certificate did not replay exactly")
    q12 = F(result["history"][11]["q_classical_upper"])
    if not q12 < F(9, 200) or not F(169, 80)*F(9, 200) < F(1, 10):
        raise ArithmeticError("classical contraction witness failed")
    witness = F(99, 100)
    update = t.all_plus_boundary_update(witness, F(13, 20))
    if update <= witness:
        raise ArithmeticError("worst-boundary countercontrol failed")
    names = ("tree_duality.py", "test_tree_duality.py", "make_receipt.py",
             "reference_frontier.json", "TREE_DUALITY.md", "HANDOFF.md")
    return {
        "status": "local_unreviewed_tree_identity_not_finite_graph_sampling",
        "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                          for name in names},
        "reference_source_sha256": reference["source_sha256"],
        "reference_artifact_sha256": reference["artifact_sha256"],
        "exact_quantum_reference_entries_replayed": len(replay),
        "bounded_tree": result,
        "clean_classical_certificate": {
            "level": 12, "q_upper_strictly_below": "9/200",
            "recurrence_coefficient": "169/80", "scaled_q_upper": "1521/16000",
            "scaled_q_upper_strictly_below": "1/10",
            "bound": "q_(12+s) <= (80/169)*(1/10)^(2^s), s>=0",
            "scope": "original_unrounded_free_boundary_tree_recursion"},
        "worst_boundary_countercontrol": {
            "m": str(witness), "update_exact": str(update),
            "update_greater_than_m": True, "retained_magnetization_lower": str(witness),
            "scope": "ferromagnetic_gauge_all_plus_tree_boundary_only"},
        "finite_graph_classical_mixing_time_upper": None,
        "finite_block_quantum_error_upper": None,
        "classical_fixed_instance_sampler_constructed": False,
        "global_quantum_decoders_excluded": False,
        "new_algorithm_or_speedup": False,
        "decision": "deprioritize_tree_success_as_a_reconstruction_barrier_crossing",
        "next_test": "global_affine_filter_vs_matched_positive_classical_sampler",
        "prior_art": ["https://arxiv.org/abs/1701.05583",
                      "https://arxiv.org/html/2609.05857v1",
                      "https://arxiv.org/html/2609.40345v1"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = report()
    if args.write:
        (HERE/"receipt.json").write_bytes(encoded(result))
    if args.output:
        args.output.write_bytes(encoded(result))
    print(json.dumps({"status": result["status"],
                      "reference_entries_replayed": result["exact_quantum_reference_entries_replayed"],
                      "first_classical_basin_level": result["bounded_tree"]["nonreconstruction_certificate"]["level"],
                      "finite_graph_sampler": "UNKNOWN"}, sort_keys=True))
