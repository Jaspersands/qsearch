"""Scoped obstruction to fixed-direction, all-outcome carry extraction.

LOCAL DERIVATION / REVIEW PENDING. Not a general quantum lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import networkx as nx

from dcp_carry_packets import binary_rank, compile_packet, single_packet_source_bound


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_carry_throughput_gate.json"


def physical_directions(packet, directions):
    directions = tuple(directions)
    k = packet.retained_qubits
    if any(not 0 < u < 1 << k for u in directions):
        raise ValueError("logical direction out of range")
    if binary_rank(directions, k) != len(directions):
        raise ValueError("independent directions required")
    return tuple(sum(((row & u).bit_count() & 1) << i
                     for i, row in enumerate(packet.kernel_rows)) for u in directions)


def fixed_direction_conductor_gate(packet, directions):
    """Necessary, not sufficient, for product output on EVERY background."""
    if packet.modulus < 8:
        raise ValueError("higher-carry conductor gate requires modulus >=8")
    physical = physical_directions(packet, directions)
    graph = nx.Graph()
    graph.add_nodes_from(range(packet.input_qubits))
    graph.add_edges_from(packet.cnot_schedule())
    blocks = tuple(sum(1 << i for i in component)
                   for component in nx.connected_components(graph))
    failures = []
    for i, j in itertools.combinations(range(len(physical)), 2):
        overlap = physical[i] & physical[j]
        if any(overlap & block not in (0, block) for block in blocks):
            failures.append([i, j])
    return {"necessary_gate_passed": not failures,
            "sufficient_product_output_certificate": False,
            "conductor_component_count": len(blocks),
            "violating_direction_pairs": failures,
            "fixed_directions_all_complement_outcomes_only": True,
            "general_quantum_lower_bound": False}


def calibration_product_on_background(packet, directions, background):
    """Independent bounded affine-identity control, not an extraction algorithm."""
    directions = tuple(directions)
    physical_directions(packet, directions)
    k = packet.retained_qubits
    if k > 8:
        raise ValueError("bounded calibration requires k<=8")
    if not 0 <= background < 1 << k:
        raise ValueError("background out of range")
    modulus = packet.modulus // 2
    origin = packet.residual(background)
    labels = [tuple((a - b) % modulus for a, b in
                    zip(packet.residual(background ^ u), origin)) for u in directions]
    for assignment in range(1 << len(directions)):
        z = background
        for j, u in enumerate(directions):
            if assignment >> j & 1:
                z ^= u
        predicted = tuple((origin[l] + sum(labels[j][l] for j in range(len(directions))
                                         if assignment >> j & 1)) % modulus
                          for l in range(packet.dimension))
        if predicted != packet.residual(z):
            return False
    return True


def q8_postselection_ledger(packet, directions):
    """Exact fixed-U acceptance law, conditional on this packet's syndrome.

    Outcomes are uniform. Product extraction must work for EVERY secret;
    this is not permission to draw the accepted source at unit cost.
    """
    if packet.modulus != 8:
        raise ValueError("postselection ledger requires modulus eight")
    physical = physical_directions(packet, directions)
    parity = [sum((a & 1) << i for i, a in enumerate(row)) for row in packet.labels]
    k = packet.retained_qubits
    rows, targets = [], []
    for i, j in itertools.combinations(range(len(physical)), 2):
        overlap = physical[i] & physical[j]
        for l, component in enumerate(packet.labels):
            constant = sum((1 - 2 * packet.origin[h]) * a
                           for h, a in enumerate(component) if overlap >> h & 1)
            if constant & 1:
                return {"possible": False, "reason": "quadratic parity obstruction",
                        "success_probability": {"numerator": "0", "denominator": "1"}}
            row = packet.logical_z_mask(parity[l] & overlap)
            if any((row & u).bit_count() & 1 for u in directions):
                return {"possible": False, "reason": "cubic interaction on retained subspace",
                        "success_probability": {"numerator": "0", "denominator": "1"}}
            rows.append(row)
            targets.append(constant // 2 & 1)
    rank = binary_rank(rows, k)
    augmented_rank = binary_rank([row | (target << k) for row, target in zip(rows, targets)], k + 1)
    possible = rank == augmented_rank
    return {"possible": possible,
            "reason": "linear complement constraints" if possible else "inconsistent complement constraints",
            "constraint_rank": rank, "retained_product_outputs_if_accepted": len(directions),
            "logical_constraint_rows": rows, "constraint_targets": targets,
            "success_probability": {"numerator": "1" if possible else "0",
                                    "denominator": str(1 << rank) if possible else "1"},
            "inverse_success_batches": str(1 << rank) if possible else None,
            "conditioned_output_labels_proved_iid": False,
            "syndrome_conditioned_not_native_average": True,
            "free_postselection": False}


def native_fixed_yield_bound(n):
    """Universal over label-dependent fixed bases; native m=3n, q>=8."""
    if n < 1:
        raise ValueError("positive dimension required")
    m = 3 * n
    w = m // 32
    distance_failure = Fraction(sum(math.comb(m, j) for j in range(1, w + 1)), 1 << n)
    # The earlier bound also charges an unnecessary even-row event; keeping
    # that slack is conservative for the connected-conductor event here.
    old = single_packet_source_bound(n)
    encoded = old["public_guaranteed_single_packet_equation_probability_upper_bound"]
    conductor_failure = Fraction(int(encoded["numerator_hex"], 16),
                                 1 << encoded["denominator_binary_exponent"])
    failure = min(Fraction(1), distance_failure + conductor_failure)
    def dyadic(value):
        return {"numerator_hex": hex(value.numerator),
                "denominator_binary_exponent": value.denominator.bit_length() - 1}
    return {"dimension": n, "input_qubits": m, "modulus_condition": "power of two >=8",
            "source": "unconditional IID uniform vector labels",
            "short_kernel_weight_threshold": w,
            "fixed_all_outcome_product_output_cap": m // (w + 1),
            "cap_is_at_most_31": m // (w + 1) <= 31,
            "distance_failure_bound": dyadic(distance_failure),
            "conductor_failure_bound": dyadic(conductor_failure),
            "cap_failure_probability_upper_bound": dyadic(failure),
            "bound_vacuous": failure == 1,
            "outcome_adaptive_direction_selection_covered": False,
            "general_quantum_measurements_covered": False}


def run_controls():
    implication_checks = 0
    accepted_pair_checks = 0
    ledger_checks = 0
    for n, m, alphabet in ((1, 3, range(8)), (2, 3, range(2))):
        for flat in itertools.product(alphabet, repeat=n * m):
            labels = [flat[l * m:(l + 1) * m] for l in range(n)]
            first = compile_packet(labels, 8)
            for syndrome in range(1 << len(first.pivots)):
                packet = compile_packet(labels, 8, syndrome)
                for u, v in itertools.combinations(range(1, 1 << packet.retained_qubits), 2):
                    directions = (u, v)
                    # Two distinct nonzero binary vectors are independent.
                    gate = fixed_direction_conductor_gate(packet, directions)
                    outcomes = [calibration_product_on_background(packet, directions, z)
                                for z in range(1 << packet.retained_qubits)]
                    actual = all(outcomes)
                    ledger = q8_postselection_ledger(packet, directions)
                    probability = ledger["success_probability"]
                    assert Fraction(sum(outcomes), len(outcomes)) == Fraction(
                        int(probability["numerator"]), int(probability["denominator"]))
                    ledger_checks += 1
                    assert not actual or gate["necessary_gate_passed"]
                    implication_checks += 1
                    accepted_pair_checks += actual
    labels = [[1, 3, 1, 3, 1, 3]]
    directions = (7, 25)
    packet = compile_packet(labels, 8)
    assert calibration_product_on_background(packet, directions, 0)
    failing_backgrounds = [z for z in range(1 << packet.retained_qubits)
                           if not calibration_product_on_background(packet, directions, z)]
    assert failing_backgrounds
    assert not fixed_direction_conductor_gate(packet, directions)["necessary_gate_passed"]
    ledger = q8_postselection_ledger(packet, directions)
    assert ledger["possible"] and ledger["constraint_rank"] == 1
    assert len(failing_backgrounds) == 16
    assert all(calibration_product_on_background(compile_packet(labels, 4), directions, z)
               for z in range(1 << packet.retained_qubits))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "exhaustive_implication_checks": implication_checks,
            "exhaustive_postselection_probability_checks": ledger_checks,
            "all_outcome_product_pairs_retained": accepted_pair_checks,
            "zero_background_false_positive": {
                "labels": labels, "modulus": 8, "logical_directions": list(directions),
                "zero_background_passes": True,
                "failing_backgrounds": failing_backgrounds,
                "postselection_ledger": ledger,
                "same_directions_valid_at_modulus_four": True},
            "native_source_bounds": [native_fixed_yield_bound(n) for n in (8, 16, 32, 64, 128)],
            "scope": "fixed directions within one parity packet; all complement outcomes; all secrets",
            "uniform_pure_product_approximation_gate": {
                "strict_trace_error_threshold": "sin(pi/8)",
                "worst_secret_witness": "(q/8)e_l",
                "constant_one_qubit_eigenvalue_ceiling": "(1+1/sqrt(2))/2",
                "average_branch_or_secret_error_covered": False,
                "mixed_product_targets_use_same_trace_threshold": False,
                "independent_theorem_review": False},
            "outcome_adaptive_or_correlated_decoder_excluded": False,
            "dependency_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py")},
            "independently_reviewed_theorem": False,
            "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "exhaustive_implication_checks", "all_outcome_product_pairs_retained",
                       "scope", "speedup_claim_allowed")}, indent=2))


if __name__ == "__main__":
    main()
