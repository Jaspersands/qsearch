"""Exact balanced-product noise law and noise-aware adaptive packet policies.

Independent original phase dephasing is a PREMISE, not established by labels,
small simulations, or per-register marginals. No noisy full decoder is supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import networkx as nx

from theorems.dcp_adaptive_affine_packet_receiver import (
    REPORT as AFFINE_REPORT, execute_public_policy, exact_json, is_useful_descent, output_label, points,
)
from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic, dyadic, integer


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_affine_packet_noise.json"
CONTRACT = ROOT / "research/hypotheses/dcp_affine_packet_noise_contract.json"
MODEL = "independent-balanced-original-phase-depolarization"


def validate_visibilities(visibilities, source_model=MODEL):
    if source_model != MODEL:
        raise ValueError("independent balanced original-input noise premise required")
    visibilities = tuple(visibilities)
    if any(type(v) not in (int, Fraction) for v in visibilities):
        raise ValueError("exact integer/Fraction visibilities required, not float or boolean")
    visibilities = tuple(Fraction(v) for v in visibilities)
    if not visibilities or any(not 0 <= v <= 1 for v in visibilities):
        raise ValueError("visibility must lie in [0,1]")
    for v in visibilities:
        dyadic(v)  # Exact dyadic workbench, no float approximation of weights.
        if v.denominator.bit_length() > 257:
            raise ValueError("UNKNOWN: dyadic precision work cap")
    return visibilities


def pair_visibility(visibilities, direction, *, source_model=MODEL):
    visibilities = validate_visibilities(visibilities, source_model)
    integer(direction, "physical XOR direction", 1, (1 << len(visibilities)) - 1)
    value = Fraction(1)
    for i, v in enumerate(visibilities):
        if direction >> i & 1:
            value *= v
    return value


def solve_noise(case, visibilities, *, source_model=MODEL):
    """Rescore a verified affine geometry, with ALL branches still paid."""
    visibilities = validate_visibilities(visibilities, source_model)
    m = case["input_qubits"]
    if len(visibilities) != m:
        raise ValueError("one visibility per ORIGINAL source register required")
    exponent = sum(v.denominator.bit_length() - 1 for v in visibilities)
    scale = 1 << exponent
    def weight(u):
        value = scale * pair_visibility(visibilities, u)
        if value.denominator != 1:
            raise ArithmeticError("integer weight scaling failed")
        return value.numerator
    states = case["states"]
    scores, frozen, chosen = [], [], []
    for state in states:
        if state["dimension"] == 1:
            score = 2 * weight(int(state["basis_hex"][0], 16)) if state["useful_descent"] else 0
            scores.append(score)
            frozen.append(score)
            chosen.append(None)
        else:
            action = max(state["actions"], key=lambda a: (
                sum(scores[i] for i in a["children"]), -a["form"]))
            scores.append(sum(scores[i] for i in action["children"]))
            chosen.append(action["form"])
            pure_action = next(a for a in state["actions"] if a["form"] == state["chosen_form"])
            frozen.append(sum(frozen[i] for i in pure_action["children"]))
    static = []
    for root in case["static_comparator_all_syndromes"]:
        choices = [(row["good_assignments"] * weight(int(row["physical_direction_hex"], 16)),
                    int(row["physical_direction_hex"], 16)) for row in root["all_direction_scores"]]
        score, u = max(choices, key=lambda item: (item[0], -item[1]))
        static.append({"origin_hex": root["origin_hex"], "best_direction_hex": hex(u),
                       "scaled_weighted_good_assignments": score})
    labels = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
    matching_records = []
    for identifier in case["root_ids_all_syndromes"]:
        root = states[identifier]
        vertices = points(tuple(int(v, 16) for v in root["basis_hex"]), int(root["origin_hex"], 16))
        graph = nx.Graph()
        graph.add_nodes_from(vertices)
        graph.add_weighted_edges_from((x, y, weight(x ^ y)) for x in vertices for y in vertices
                                      if x < y and is_useful_descent(output_label(labels, case["phase_bits"], x, y)))
        # Integer-scaled weights keep the blossom computation exact.
        matching = sorted((min(x, y), max(x, y)) for x, y in nx.max_weight_matching(graph))
        matching_records.append({"root_id": identifier,
                                 "edges": [[x, y, weight(x ^ y)] for x, y in matching],
                                 "scaled_weight_sum": sum(weight(x ^ y) for x, y in matching)})
    roots = case["root_ids_all_syndromes"]
    adaptive = sum(scores[i] for i in roots)
    pure_frozen = sum(frozen[i] for i in roots)
    static_value = sum(s["scaled_weighted_good_assignments"] for s in static)
    arbitrary = 2 * sum(r["scaled_weight_sum"] for r in matching_records)
    if not max(pure_frozen, static_value) <= adaptive <= arbitrary:
        raise ArithmeticError("noise-aware comparator inequalities failed")
    leaves = []
    def collect(i):
        state = states[i]
        if state["dimension"] == 1:
            leaves.append(i)
            return
        action = next(a for a in state["actions"] if a["form"] == chosen[i])
        for child in action["children"]:
            collect(child)
    for root in roots:
        collect(root)
    good_pairs = sum(states[i]["useful_descent"] for i in leaves)
    # For this exact PRODUCT model, ideal product state is a joint eigenvector.
    pure_product_mass = Fraction(1)
    for v in visibilities:
        pure_product_mass *= (1 + v) / 2
    return {
        "source_model": source_model, "source_independence_established_by_workflow": False,
        "actual_lattice_noise_matched": False,
        "visibility_by_original_register": [dyadic(v) for v in visibilities],
        "integer_visibility_scale_exponent": exponent,
        "scaled_optimal_weighted_good_assignments_by_state": scores,
        "chosen_form_by_state": chosen, "chosen_leaf_ids": leaves,
        "noise_aware_best_static": static, "arbitrary_weighted_pairings": matching_records,
        "noise_aware_useful_retained_visibility": dyadic(Fraction(adaptive, 1 << (m + exponent))),
        "frozen_pure_policy_useful_retained_visibility": dyadic(Fraction(pure_frozen, 1 << (m + exponent))),
        "noise_aware_best_static_useful_retained_visibility": dyadic(Fraction(static_value, 1 << (m + exponent))),
        "arbitrary_pairing_useful_retained_visibility_upper_bound": dyadic(Fraction(arbitrary, 1 << (m + exponent))),
        "useful_label_probability_under_selected_noisy_policy": dyadic(Fraction(2 * good_pairs, 1 << m)),
        "exact_product_input_trace_distance_from_ideal": dyadic(1 - pure_product_mass),
        "all_measurement_branch_probabilities_unchanged": True,
        "visibility_exponent_is_physical_Hamming_distance_not_merge_depth": True,
        "retained_visibility_is_complete_decoder_success": False,
    }


def execute_noise_policy(case, noisy, port):
    """Only public policy choices change; source ownership stays with port."""
    state_copy = [dict(s, chosen_form=form) for s, form in zip(case["states"], noisy["chosen_form_by_state"])]
    receipt = execute_public_policy(dict(case, states=state_copy), port)
    leaf = case["states"][receipt["leaf_id"]]
    visibilities = tuple(decode_dyadic(v) for v in noisy["visibility_by_original_register"])
    receipt["conditional_visibility_UNDER_PRODUCT_PROMISE"] = dyadic(pair_visibility(visibilities,
                                                                                     int(leaf["basis_hex"][0], 16)))
    return receipt


def correlation_counterexample():
    matrix = [[int((x.bit_count() - y.bit_count()) % 2 == 0) for y in range(8)] for x in range(8)]
    pair_visibility = Fraction(2 * matrix[0][3], matrix[0][0] + matrix[3][3])
    return {
        "source": "Equal mixture of |+>^m and Z^tensor_m|+>^m, m=3",
        "individual_phase_visibilities": [0, 0, 0],
        "retained_pair": [0, 3],
        "joint_density_numerators_denominator_8": matrix,
        "actual_even_weight_pair_visibility": dyadic(pair_visibility),
        "incorrect_product_of_marginals_prediction": dyadic(0),
        "correlation_covered_by_product_noise_law": False,
        "flat_diagonal_alone_implies_visibility_factorization": False,
    }


def build_report():
    raw = AFFINE_REPORT.read_bytes()
    source = json.loads(raw)
    selected = [("unfiltered-seed-2", source["source_controls"][2]),
                ("unfiltered-seed-5", source["source_controls"][5]),
                ("selected-grammar-gap-94", source["affine_grammar_gap_counterexample"])]
    cases = []
    for key, case in selected:
        grid = [(str(v), (v,) * case["input_qubits"])
                for v in (Fraction(1), Fraction(15, 16), Fraction(3, 4), Fraction(1, 2), Fraction(0))]
        grid.append(("heterogeneous", tuple((Fraction(1), Fraction(1, 2), Fraction(3, 4))[i % 3]
                                             for i in range(case["input_qubits"]))))
        for name, visibility in grid:
            cases.append(dict(source_control=key, noise_setting=name, **solve_noise(case, visibility)))
    contract = json.loads(CONTRACT.read_text())
    return exact_json({
        "status": "EXACT_PRODUCT_NOISE_PACKET_LAW_NOT_LATTICE_NOISE_CERTIFICATE",
        "contract_id": contract["contract_id"],
        "source_geometry_artifact": str(AFFINE_REPORT.relative_to(ROOT)),
        "source_geometry_sha256": hashlib.sha256(raw).hexdigest(),
        "noise_controls": cases, "correlation_counterexample": correlation_counterexample(),
        "scope": contract["scope"], "remaining_proof_obligations": contract["remaining_proof_obligations"],
        "accepted_speedup_candidate": False, "efficient_receiver_supplied": False,
        "source_quantum_preparations_executed": 0,
    })


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "noise_controls": len(report["noise_controls"]),
                      "actual_lattice_noise_matched": False, "accepted_speedup_candidate": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
