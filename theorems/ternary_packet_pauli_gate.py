"""Conditional native packet Pauli visibility, not a general receiver no-go.

LOCAL DERIVATION / REVIEW PENDING. Low-frame-defined probes have an exact
high-lift second moment. High-informed implicit search and collective
measurements are outside the gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import nmod_mat

from cyclotomic_fiber_receiver import inverse_frequency_coordinates
from ternary_carry_packets import compile_packet
from ternary_correlated_packet_acquisition import integer, word

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_packet_pauli_gate.json"
DERIVATION = ROOT / "research/TERNARY_PACKET_PAULI_GATE.md"


def rank(rows, width):
    return nmod_mat(rows, 3).rank() if rows else 0


def kernel_frame(packet):
    h = packet.retained
    if not h:
        raise ValueError("nonempty retained kernel frame required")
    base = packet.assignment((0,)*h)
    columns = []
    for j in range(h):
        e = tuple(int(i == j) for i in range(h))
        columns.append(tuple((a-b) % 3 for a, b in zip(packet.assignment(e), base)))
    return tuple(tuple(column[i] for column in columns) for i in range(packet.consumed))


def probe_record(packet, translation, diagonal):
    h = packet.retained
    translation, diagonal = word(translation, h), word(diagonal, h)
    if not any(translation):
        raise ValueError("nonzero logical translation required; flat diagonal probes are secret-blind")
    D = kernel_frame(packet)
    physical = tuple(sum(a*v for a, v in zip(row, translation)) % 3 for row in D)
    support = tuple(i for i, a in enumerate(physical) if a)
    projected = tuple(D[i] for i in support)
    b = rank(projected, h)
    in_span = rank(projected+(diagonal,), h) == b
    return {"logical_translation": translation, "logical_diagonal": diagonal,
            "physical_translation": physical, "translated_physical_support": support,
            "restricted_kernel_frame_rank": b, "diagonal_in_restricted_row_span": in_span,
            "conditional_high_lift_squared_overlap_mean": str(Fraction(1, 3**b) if in_span else Fraction(0)),
            "outside_span_overlap_identically_zero_for_each_high_lift": not in_span,
            "conditioned_low_frame_and_syndrome": True,
            "nonzero_residual_secret_required": True,
            "probe_choice_low_only_policy_verified_by_this_function": False,
            "scope": "A(v,w)=<psi|Z^w X^(-v)|psi>; fixed low-frame-defined v,w over IID odd high lifts",
            "general_collective_receiver_or_high_informed_search_excluded": False}


def distance_control(packet):
    D, h, K = kernel_frame(packet), packet.retained, packet.consumed
    if h > 8 or len(packet.pivots) > 8:
        raise ValueError("exact code distance control capped at eight free/dual coordinates")
    directions = [v for v in product(range(3), repeat=h) if any(v)]
    physical = [tuple(sum(a*x for a, x in zip(row, v)) % 3 for row in D) for v in directions]
    primal = min(sum(bool(x) for x in row) for row in physical)
    dual_words = [tuple(sum(a*row[i] for a, row in zip(u, packet.reduced_rows)) % 3 for i in range(K))
                  for u in product(range(3), repeat=len(packet.pivots)) if any(u)]
    dual = min((sum(bool(x) for x in row) for row in dual_words), default=K+1)
    bound = min(primal, dual-1)
    actual = min(probe_record(packet, v, (0,)*h)["restricted_kernel_frame_rank"] for v in directions)
    if actual < bound:
        raise ArithmeticError("kernel/dual-distance projection rank bound failed")
    return {"native_labels": packet.labels, "odd_level": packet.level, "syndrome": packet.syndrome,
            "RREF_rows": packet.reduced_rows, "kernel_frame": D,
            "primal_minimum_distance": primal, "dual_minimum_distance_or_K_plus_one": dual,
            "all_nonzero_translation_rank_lower_bound": bound,
            "exact_minimum_translation_rank": actual, "all_logical_directions_checked": len(directions),
            "distance_enumeration_is_scalable_algorithm": False}


def population_envelope(n, K, distance, menu_size):
    integer(n, "secret dimension", 1); integer(K, "odd input count", n+1)
    integer(distance, "distance threshold", 2); integer(menu_size, "low-defined probe menu size", 1)
    if distance > K:
        raise ValueError("distance threshold must not exceed code length")
    numerator = sum(math.comb(K, w)*2**(w-1) for w in range(1, distance))
    primal = Fraction(numerator, 3**n)
    dual = Fraction((3**n-1)*numerator, 3**K)
    bad = min(Fraction(1), primal+dual)
    b = distance-1
    good_menu = min(Fraction(1), Fraction(menu_size, 3**b))
    raw = min(Fraction(1), bad+good_menu)
    return {"dimension": n, "odd_input_count": K, "distance_threshold": distance,
            "minimum_restricted_rank_on_good_sources": b, "low_defined_menu_size": menu_size,
            "primal_distance_failure_union_bound": str(min(Fraction(1), primal)),
            "dual_distance_failure_union_bound": str(min(Fraction(1), dual)),
            "combined_bad_low_source_probability_upper": str(bad),
            "good_source_menu_squared_overlap_mean_upper": str(good_menu),
            "raw_population_menu_squared_overlap_mean_upper": str(raw),
            "one_Pauli_test_mean_total_variation_to_unbiased_upper_squared": str(raw/4),
            "fresh_B_packet_transcript_TV_upper_squared_before_clipping": "B^2*raw_bound/4",
            "full_row_rank_conditioning_assumed": False,
            "menu_can_be_selected_from_high_labels_after_low_only_definition": True,
            "implicit_high_informed_exponential_probe_families_covered": False,
            "multiple_noncommuting_measurements_on_same_packet_covered": False,
            "generic_quantum_complexity_lower_bound": False}


def conditional_census(low, translation, diagonal, syndrome):
    """Complete level3 high lifts, with exact F3 character-moment counts."""
    K = len(low)
    if not 1 <= K <= 3 or any(type(x) is not int or x not in range(3) for x in low):
        raise ValueError("bounded one-component conditional census, at most three odd inputs")
    labels = [[inverse_frequency_coordinates(a, 2*a % 3, 3)] for a in low]
    packet = compile_packet(labels, 3, syndrome)
    probe = probe_record(packet, translation, diagonal)
    points = tuple(product(range(3), repeat=packet.retained))
    shifted = tuple(tuple((z+v) % 3 for z, v in zip(point, translation)) for point in points)
    assignments = tuple(packet.assignment(z) for z in points)
    targets = tuple(packet.assignment(z) for z in shifted)
    histogram, tables, maximum = Counter(), [], 0.
    for high in product(range(3), repeat=2*K):
        pairs = [(a+3*high[2*i], (2*a % 3)+3*high[2*i+1]) for i, a in enumerate(low)]
        phase = []
        for z, t, target in zip(points, assignments, targets):
            difference = sum((pairs[i][b-1] if b else 0)-(pairs[i][a-1] if a else 0)
                             for i, (a, b) in enumerate(zip(t, target))) % 9
            if difference % 3:
                raise ArithmeticError("logical translation left the original syndrome fiber")
            phase.append((difference//3+sum(a*b for a, b in zip(diagonal, z))) % 3)
        tables.append(phase)
        histogram.update((a-b) % 3 for a in phase for b in phase)
        overlap = sum(complex(math.cos(2*math.pi*x/3), math.sin(2*math.pi*x/3)) for x in phase)/len(phase)
        maximum = max(maximum, abs(overlap))
    denominator = len(tables)*len(points)**2
    if histogram[1] != histogram[2]:
        raise ArithmeticError("character average is not a real rational moment")
    moment = Fraction(histogram[0]-histogram[2], denominator)
    if moment != Fraction(probe["conditional_high_lift_squared_overlap_mean"]):
        raise ArithmeticError("exact complete native high lifts falsified the overlap formula")
    if probe["outside_span_overlap_identically_zero_for_each_high_lift"] and maximum > 3e-12:
        raise ArithmeticError("a forbidden Fourier character survived on a kernel fiber")
    return {"low_first_frequency_rows": low, "prototype_native_labels": packet.labels,
            "syndrome": packet.syndrome, "probe": probe, "kernel_frame": kernel_frame(packet),
            "complete_high_lift_assignments": len(tables), "logical_words_per_lift": len(points),
            "exact_character_difference_histogram": [histogram[i] for i in range(3)],
            "character_average_denominator": denominator, "exact_squared_overlap_mean": str(moment),
            "all_phase_tables_sha256": hashlib.sha256(json.dumps(tables, separators=(",", ":")).encode()).hexdigest(),
            "maximum_single_lift_overlap_magnitude": maximum,
            "identical_packet_factory_supplied": False, "quantum_speedup_proved": False}


def run_controls():
    censuses = [conditional_census([1, 1, 1], (1, 0), (0, 0), (1,)),
                conditional_census([1, 1, 0], (1, 0), (0, 0), (1,)),
                conditional_census([1, 1, 0], (1, 0), (0, 1), (1,))]
    distances = []
    for low in product(range(3), repeat=3):
        labels = [[inverse_frequency_coordinates(a, 2*a % 3, 3)] for a in low]
        distances.append(distance_control(compile_packet(labels, 3)))
    return {"status": "CORRELATED_PACKET_LOW_DEFINED_PAULI_VISIBILITY_GATE_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "complete_conditional_censuses": censuses, "complete_small_low_matrix_distance_controls": distances,
            "analytic_population_envelopes": [population_envelope(n, 2*n, n//8, n*n) for n in (32, 64, 128, 256, 1024)],
            "candidate_record_accepted": False, "general_receiver_no_go_claimed": False,
            "quantum_speedup_proved": False,
            "research_decision": "Low-defined polynomial Pauli menus are weak in constant-rate random native kernel packets. Seek high-informed implicit observables or coherent noncommuting receivers, not more expectation estimation of these probes.",
            "routine_CLI_registry_and_Git_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "complete_high_lifts": sum(c["complete_high_lift_assignments"] for c in report["complete_conditional_censuses"])}, indent=2))


if __name__ == "__main__":
    main()
