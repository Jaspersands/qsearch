"""Fixed-address bounded signed-list tree with clean XOR-F interpretation.

This is a costed reversible classical program on basis wires, not a hardware
gate export, free QRAM, known-best sieve, or completed DCP decoder.
"""
from __future__ import annotations

import argparse
from itertools import islice
import json
from math import comb
from pathlib import Path
from random import Random

from dcp_affine_marked_pairing import affine_hash
from dcp_balanced_pairing import block_masks, evaluate_record_join, sort_records, unsort_records
from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_native_tree_moment_audit import dimensions, overflow_contract
from theorems.dcp_vector_short_mask_join import packed_group_value


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_native_tree_receiver.json"
CONTRACT = ROOT / "research/hypotheses/dcp_native_tree_receiver_contract.json"
KIND = "NATIVE_Z4_BOUNDED_TREE_SORT_JOIN"
CONTRACT_ID = "native_Z4_bounded_tree_clean_XOR_F_v1"
INVALID = (1, 0, 0)  # (invalid, physical support ID, packed componentwise sum)


def resources(depth, chunk, block_width=None, capacity=None):
    k, L, n = dimensions(depth, chunk)
    B = 4 * chunk if block_width is None else block_width
    integer(B, "physical leaf block width", 1, 4096)
    m = k * B
    integer(m, "original register count", 2, 4096)
    w = next((w for w in range(1, B + 1) if comb(B, w) >= L), None)
    if w is None:
        raise ValueError("leaf block has too few distinct fixed nonempty supports")
    bound = overflow_contract(depth, chunk)
    recommended = int(bound["intermediate_list_capacity_hex"], 16)
    C = recommended if capacity is None else capacity
    integer(C, "nonroot list capacity", L)
    sizes = [L]
    levels = []
    for level in range(1, depth):
        cells = sizes[-1] ** 2
        retained = min(C, cells)
        padded = 1 << (cells - 1).bit_length()
        bits = padded.bit_length() - 1
        comparisons = padded * bits * (bits + 1) // 4
        levels.append({"level": level, "nodes": k >> level,
                       "child_slots": sizes[-1], "candidate_cells": cells,
                       "padded_cells": padded, "retained_slots": retained,
                       "forward_comparators": comparisons})
        sizes.append(retained)
    S = sizes[-1]
    padded = 1 << (2 * S - 1).bit_length()
    bits = padded.bit_length() - 1
    root_comparisons = padded * bits * (bits + 1) // 4
    g = bound["hash_bits"]
    key_bits = 2 * n + g + 1
    counter_bits = (S * S).bit_length()
    record_bits = key_bits + 2 + m
    scan_bits = key_bits + 3 * counter_bits + 3 * m
    root_workspace = padded * record_bits + (padded + 1) * scan_bits + root_comparisons
    root = {"padded_records": padded, "persistent_workspace_bits": root_workspace}
    node_count = k - 2
    # All levels stay live until the root copy has been reversed. Prefix counts
    # and compare flags are wires, not erased classical side information.
    workspace = k * L * (1 + m + 2 * n) + root_workspace
    workspace += (node_count + 1) * max(1, (node_count + 1).bit_length()) + node_count
    for row in levels:
        N, P, slots = row["candidate_cells"], row["padded_cells"], row["retained_slots"]
        per_node = (P + slots) * (1 + m + 2 * n)
        per_node += (P + 1) * (N + 1).bit_length() + row["forward_comparators"]
        workspace += row["nodes"] * per_node
    candidate_cells = sum(r["nodes"] * r["candidate_cells"] for r in levels)
    comparators = 2 * root_comparisons + sum(2 * r["nodes"] * r["forward_comparators"] for r in levels)
    scans = 2 * padded + sum(2 * r["nodes"] * r["padded_cells"] for r in levels)
    return {"depth": depth, "chunk_components": chunk, "components": n,
            "leaf_count": k, "leaf_list_length": L, "block_width": B,
            "original_registers": m, "leaf_support_weight": w,
            "physical_mask_width": k * w, "capacity": C,
            "recommended_capacity": recommended, "hash_bits": g,
            "public_affine_seed_bits": g * (m + 1), "nonroot_levels": levels,
            "root_child_slots": S, "root_join": root,
            "one_XOR_F_candidate_cell_evaluations": 2 * candidate_cells,
            "one_XOR_F_leaf_record_evaluations": 2 * k * L,
            "one_XOR_F_root_record_evaluations": 4 * S,
            "one_XOR_F_comparators": comparators, "one_XOR_F_list_scan_steps": scans,
            "one_XOR_F_retained_record_copies": 2 * sum(r["nodes"] * r["retained_slots"] for r in levels),
            "one_XOR_F_overflow_prefix_steps": 2 * node_count,
            "persistent_workspace_bits": workspace,
            "accepted_six_XOR_F_comparators": 6 * comparators,
            "failed_four_XOR_F_comparators": 4 * comparators,
            "compiler_live_qubits_excluding_arithmetic_scratch": workspace + 3*m + 4,
            "polynomial_arithmetic_scratch_excluded": True,
            "overflow_is_seed_independent": True,
            "moment_overflow_lower_bound_applicable": C >= recommended,
            "moment_coarse_lower_bound_IF_source_premises": bound["coarse_mass_lower_IF_clean_exact_receiver_contract"] if C >= recommended else None,
            "coherent_RAM_assumed": False, "hardware_gate_export_implemented": False,
            "abstract_clean_basis_wire_interpreter_implemented": True,
            "time_and_space_form": "O(k*C^2*poly(n,m,log C)); fixed-address histories retained",
            "one_output_recursion_supply_removed": False}


def make_program(labels, depth, chunk, seed=0, capacity=None):
    A = matrix(labels)
    k, _, n = dimensions(depth, chunk)
    if len(A) != n or len(A[0]) % k:
        raise ValueError("native tree requires n=b(a+1) and disjoint equal leaf blocks")
    R = resources(depth, chunk, len(A[0]) // k, capacity)
    integer(seed, "complete unconditioned affine seed", 0, (1 << R["public_affine_seed_bits"]) - 1)
    m, g = R["original_registers"], R["hash_bits"]
    return {"kind": KIND, "width": m, "depth": depth, "chunk_components": chunk,
            "descent_bits": 2, "coarse_labels": [[a % 4 for a in row] for row in A],
            "capacity": R["capacity"], "hash_rows_hex": [hex((seed >> (j*m)) & ((1 << m)-1)) for j in range(g)],
            "hash_offset_hex": hex(seed >> (g*m)), "resource_ledger": R,
            "selection_access": "coarse-labels-and-independent-unfiltered-affine-seed",
            "overflow_policy": "REJECT_WHOLE_ATTEMPT",
            "seed_conditioned_on_success": False, "uniform_efficient_program_supplied": False,
            "table_lookup_is_a_free_coherent_oracle": False}


def validate_program(P):
    if P.get("kind") != KIND or P.get("descent_bits") != 2:
        raise ValueError("native Z4 bounded tree program required")
    A = matrix(P["coarse_labels"])
    k, _, n = dimensions(P["depth"], P["chunk_components"])
    if len(A) != n or len(A[0]) % k or any(a > 3 for row in A for a in row):
        raise ValueError("canonical native coarse matrix required")
    R = resources(P["depth"], P["chunk_components"], len(A[0]) // k, P["capacity"])
    m, g = R["original_registers"], R["hash_bits"]
    H = tuple(int(h, 16) for h in P["hash_rows_hex"])
    c = int(P["hash_offset_hex"], 16)
    if type(P.get("width")) is not int or P["width"] != m or len(H) != g or any(h < 0 or h >= 1 << m for h in H) or not 0 <= c < 1 << g:
        raise ValueError("canonical width and full affine hash required")
    if (P.get("resource_ledger") != R or P.get("overflow_policy") != "REJECT_WHOLE_ATTEMPT"
            or P.get("selection_access") != "coarse-labels-and-independent-unfiltered-affine-seed"
            or P.get("seed_conditioned_on_success") is not False
            or P.get("uniform_efficient_program_supplied") is not False
            or P.get("table_lookup_is_a_free_coherent_oracle") is not False):
        raise ValueError("capacity, access, whole-attempt rejection and cost contract cannot be waived")
    return A, R, H, c


def _leaf(A, x, start, B, w, L):
    return [(0, u, packed_group_value(tuple(sum(a*(1-2*(x >> i & 1)) for i, a in enumerate(row) if u >> i & 1) % 4 for row in A)))
            for u in islice(block_masks(start, B, w), L)]


def _candidates(left, right, level, chunk, n):
    for il, u, a in left:
        for ir, v, b in right:
            value = tuple(((a >> (2*j) & 3) + (b >> (2*j) & 3)) % 4 for j in range(n))
            valid = not (il or ir or any(value[(level-1)*chunk:level*chunk]))
            yield (0, u ^ v, packed_group_value(value)) if valid else INVALID


def evaluate_xor(P, x, output=0):
    A, R, H, c = validate_program(P)
    m, n, k, L = R["original_registers"], R["components"], R["leaf_count"], R["leaf_list_length"]
    integer(x, "input basis assignment", 0, (1 << m)-1)
    integer(output, "XOR target wires", 0, (1 << (m+1))-1)
    cells = R["one_XOR_F_candidate_cell_evaluations"] // 2
    if cells + R["root_join"]["padded_records"] + k*L > 100000 or (k*L*m*n > 2000000):
        raise ValueError("UNKNOWN: fixed-address interpreter work cap; not a research negative result")
    leaves = [_leaf(A, x, j*R["block_width"], R["block_width"], R["leaf_support_weight"], L) for j in range(k)]
    current = leaves
    history = []
    overflow_prefix = [0]
    overflow_flags = []
    candidate_evaluations = comparators = scans = copies = 0
    for spec in R["nonroot_levels"]:
        next_level = []
        for j in range(0, len(current), 2):
            left, right = current[j:j+2]
            records = list(_candidates(left, right, spec["level"], P["chunk_components"], n))
            candidate_evaluations += len(records)
            records.extend([INVALID] * (spec["padded_cells"]-len(records)))
            flags = sort_records(records)
            comparators += len(flags)
            counts = [0]
            for record in records:
                counts.append(counts[-1] + (record[0] == 0))
                scans += 1
            overflow = int(counts[-1] > R["capacity"])
            overflow_flags.append(overflow)
            overflow_prefix.append(overflow_prefix[-1] + overflow)
            retained = list(records[:spec["retained_slots"]])
            copies += len(retained)
            history.append((spec, left, right, records, flags, counts, retained))
            next_level.append(retained)
        current = next_level
    padding = (1 << (2*n+len(H)), 2, 0)
    def root_records():
        for side in (0, 1):
            for invalid, mask, packed in current[side]:
                if invalid:
                    yield padding
                else:
                    values = tuple((packed >> (2*j)) & 3 for j in range(n))
                    if side:
                        values = tuple(-a % 4 for a in values)
                    yield (packed_group_value(values) << len(H)) | affine_hash(mask, H, 0), side, mask
    row = evaluate_record_join(m, x, output, root_records,
                              lambda: not overflow_prefix[-1] and affine_hash(x, H, c) == 0,
                              R["root_join"], padding)
    any_overflow = bool(overflow_prefix[-1])
    node_overflows = list(overflow_flags)
    # Reverse the copied lists before their parents, and only free zero wires.
    for spec, left, right, records, flags, counts, retained in reversed(history):
        for i in range(len(retained)):
            retained[i] = tuple(a ^ b for a, b in zip(retained[i], records[i]))
            copies += 1
        overflow_prefix[-1] ^= overflow_prefix[-2] + overflow_flags[-1]
        if overflow_prefix[-1]:
            raise ArithmeticError("overflow prefix did not uncompute")
        overflow_prefix.pop()
        overflow_flags[-1] ^= int(counts[-1] > R["capacity"])
        if overflow_flags.pop():
            raise ArithmeticError("overflow flag did not uncompute")
        for i in range(len(records)-1, -1, -1):
            counts[-1] ^= counts[-2] + (records[i][0] == 0)
            if counts.pop():
                raise ArithmeticError("list prefix count did not uncompute")
            scans += 1
        comparators += unsort_records(records, flags)
        for i, expected in enumerate(_candidates(left, right, spec["level"], P["chunk_components"], n)):
            records[i] = tuple(a ^ b for a, b in zip(records[i], expected))
            candidate_evaluations += 1
        for i in range(spec["candidate_cells"], len(records)):
            records[i] = tuple(a ^ b for a, b in zip(records[i], INVALID))
        if counts != [0] or flags or any(any(record) for record in records + retained):
            raise ArithmeticError("intermediate list work did not uncompute")
    for j, records in enumerate(leaves):
        expected = _leaf(A, x, j*R["block_width"], R["block_width"], R["leaf_support_weight"], L)
        for i, record in enumerate(expected):
            records[i] = tuple(a ^ b for a, b in zip(records[i], record))
    clean = row["workspace_clean"] and not overflow_flags and overflow_prefix == [0] and not any(any(r) for leaf in leaves for r in leaf)
    metrics = {"candidate_cell_evaluations": candidate_evaluations,
               "leaf_record_evaluations": 2*k*L,
               "root_record_evaluations": row["record_evaluations"],
               "comparators": comparators + row["comparators"],
               "list_scan_steps": scans + row["scan_steps"],
               "retained_record_copies": copies,
               "overflow_prefix_steps": 2*(k-2)}
    for key, count in metrics.items():
        if count != R["one_XOR_F_"+key]:
            raise ArithmeticError("fixed-address schedule cost omitted: "+key)
    return {"output": row["output"], "workspace_clean": clean,
            "whole_attempt_overflow": any_overflow, "node_overflows": node_overflows,
            "truncated_root_neighbor_count_not_accepted_on_overflow": row["neighbor_count_before_source_mark"],
            "persistent_workspace_bits": R["persistent_workspace_bits"], "metrics": metrics}


def propose(P, x):
    row = evaluate_xor(P, x)
    if not row["workspace_clean"]:
        raise ArithmeticError("unclean native tree program")
    size = 1 << P["width"]
    return row["output"]-size if row["output"] & size else None


def build_report():
    from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate
    rng = Random(1051603)
    controls = []
    # These are selected finite implementation controls, never source estimates.
    for depth, capacity in ((1, None), (2, 4), (2, None)):
        n, m = depth+1, 4*(1 << depth)
        A = [[rng.randrange(16) for _ in range(m)] for _ in range(n)]
        P = make_program(A, depth, 1, seed=rng.getrandbits(2*(m+1)), capacity=capacity)
        assignments = list(range(16)) + [(1 << m)-1]
        controls.append({"control_id": "depth-%d-cap-%s" % (depth, capacity),
                         "full_labels": A, "program": P,
                         "evaluations": [{"assignment": x, **evaluate_xor(P, x)} for x in assignments]})
    zeros = [[0]*16 for _ in range(3)]
    P = make_program(zeros, 2, 1, capacity=4)
    controls.append({"control_id": "zero-label-overflow-rejection", "full_labels": zeros,
                     "program": P, "evaluations": [{"assignment": x, **evaluate_xor(P, x)} for x in (0, 7, 65535)]})
    # Selected finite positive control, not an uncharged favorable seed source.
    A = [[7, 0, 0, 0, 1, 2, 6, 2], [3, 6, 3, 5, 1, 2, 0, 7]]
    P = make_program(A, 1, 1, seed=152448)
    instrument = compiler_certificate(A, 3, 2, P)
    if not instrument["pairs"]:
        raise ArithmeticError("physical positive control lost all accepted pairs")
    asymmetric = [[3,1,3,2,2,2,3,1,1,0,3,2,2,2,1,0],
                  [1,2,3,3,2,2,2,3,3,0,3,1,0,2,0,0],
                  [2,0,0,0,3,0,1,1,3,1,1,2,0,1,0,1]]
    P_asym = make_program(asymmetric, 2, 1, capacity=4)
    controls.append({"control_id": "overflow-is-not-partner-invariant", "full_labels": asymmetric,
                     "program": P_asym, "known_untruncated_edge": [2, 10368],
                     "evaluations": [{"assignment": x, **evaluate_xor(P_asym, x)} for x in (2, 10368)]})
    deep_labels = [[5,4,6,7,7,4,1,1,3,2,6,0,2,2,7,3],
                   [4,2,4,5,2,0,4,4,0,1,3,5,6,2,6,3],
                   [4,3,0,2,1,3,3,0,6,1,2,2,5,1,3,7]]
    deep_program = make_program(deep_labels, 2, 1, 1984268052846131, capacity=4)
    controls.append({"control_id": "depth-two-physical-positive-control", "full_labels": deep_labels,
                     "program": deep_program, "known_reciprocal_pair": [20, 9228],
                     "evaluations": [{"assignment": x, **evaluate_xor(deep_program, x)} for x in (20, 9228)]})
    return {"contract_id": CONTRACT_ID, "status": "CLEAN_BASIS_PROGRAM_EXTERNAL_REVIEW_PENDING",
            "finite_controls": controls, "six_call_instrument": instrument,
            "selected_controls_are_native_source_probability_estimates": False,
            "abstract_clean_basis_wire_interpreter_implemented": True,
            "hardware_gate_export_implemented": False, "source_quantum_preparations_executed": 0,
            "accepted_speedup_candidate": False, "novelty_claim": False,
            "external_theorem_review_complete": False,
            "scope": {"whole_attempt_overflow_rejection": True, "root_and_nonroot_histories_uncomputed": True,
                      "independent_uniform_coarse_labels_required_for_native_mean_bound": True,
                      "natural_source_noise_or_hardness_certified": False,
                      "one_output_recursive_supply_removed": False,
                      "improves_known_DCP_exponents": False,
                      "latent_error_comparison_used": False}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": len(report["finite_controls"]),
                      "physical_pairs": len(report["six_call_instrument"]["pairs"]),
                      "hardware_gate_export_implemented": False, "artifact": str(REPORT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
