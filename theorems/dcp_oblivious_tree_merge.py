"""Native signed-leaf controls for a reversible bounded-output oblivious join."""
from __future__ import annotations

import argparse
from itertools import islice
import json
from pathlib import Path
from random import Random

from dcp_balanced_pairing import block_masks
from dcp_oblivious_bounded_join import join_xor, schedule
from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_vector_short_mask_join import packed_group_value

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_oblivious_tree_merge.json"
CONTRACT = ROOT / "research/hypotheses/dcp_oblivious_tree_merge_contract.json"


def native_leaf_inputs(A, x, block_width=4, chunk=1):
    A = matrix(A)
    integer(chunk, "finite control chunk", 1, 1)
    integer(block_width, "finite control leaf width", 4, 4)
    n, m = len(A), len(A[0])
    integer(x, "original assignment", 0, (1 << m)-1)
    if m != 2*block_width or n < chunk:
        raise ValueError("two disjoint signed leaf blocks and a valid component chunk required")
    result = []
    for side in (0, 1):
        records = []
        for u in islice(block_masks(side*block_width, block_width, 1), 4**chunk):
            sums = tuple(sum(a*(1-2*(x >> i & 1)) for i, a in enumerate(row) if u >> i & 1) % 4 for row in A)
            key = packed_group_value(sums[:chunk] if side == 0 else tuple(-a % 4 for a in sums[:chunk]))
            payload = u | (packed_group_value(sums) << m)
            records.append((1, key, payload))
        result.append(records)
    return result


def build_report():
    rng = Random(1051604)
    A = [[rng.randrange(4) for _ in range(8)] for _ in range(3)]
    controls = []
    for x in range(16):
        left, right = native_leaf_inputs(A, x)
        for cap in (2, 4, 16):
            result = join_xor(left, right, cap, 2, 14)
            controls.append({"assignment": x, "capacity": cap, "left": left, "right": right, **result})
    frontiers = []
    for e in (4, 8, 12, 16, 32, 64):
        L = 1 << e
        # A standalone node comparison, not a source-acceptance or decoder bound.
        R = schedule(L, L, 32*L, e, 4*e)
        frontiers.append({"leaf_list_binary_exponent": e, "resource_ledger": R,
                          "cartesian_candidate_cells": L*L,
                          "fixed_sort_slots_total": sum(R["sort_sizes"]),
                          "native_probability_or_speedup_estimate": False})
    return {"status": "CLEAN_OBLIVIOUS_JOIN_EXTERNAL_REVIEW_PENDING",
            "contract_id": "native_bounded_oblivious_rank_join_v1", "native_labels": A,
            "key_bits": 2, "payload_bits": 14, "native_controls": controls,
            "symbolic_node_cost_frontiers": frontiers,
            "whole_tree_receiver_uses_this_backend": False,
            "accepted_speedup_candidate": False, "novelty_claim": False,
            "hardware_gate_export_implemented": False, "source_quantum_preparations_executed": 0,
            "basis_diagnostic_count_is_free_coherent_oracle": False,
            "literature": ["https://arxiv.org/abs/2003.09481"],
            "next_integration_contract": "Replace only nonroot Cartesian expansion; preserve native graph, whole-attempt overflow rejection, reciprocal checks and original-noise accounting."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "native_controls": len(report["native_controls"]),
                      "symbolic_frontiers": len(report["symbolic_node_cost_frontiers"]),
                      "whole_tree_backend_integrated": False, "artifact": str(REPORT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
