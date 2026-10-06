"""Nonlinear native pointed three-witness construction and cover interface.

LOCAL DERIVATION / REVIEW PENDING. The pointed finder is polynomial. The
implemented cover compiler enumerates3^m words and is NOT a fast receiver.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from cyclotomic_rescaling_gate import ideal_chart

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_pointed_triples.json"


def _integer(x, name, minimum=1):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def low_source(source):
    if source.level < 2 or source.level % 2:
        raise ValueError("native even-level integer-secret source required")
    return tuple(tuple(tuple(a % 3 for a in row) for row in item) for item in source.frequencies)


def pointed_words(frequencies, anchor):
    """A low-defined nonlinear triple containing a given classical word.

    No secret, search over assignments, unknown phase query or state copy.
    Computing this function coherently does not erase its anchor workspace.
    """
    frequencies = tuple(tuple(tuple(row) for row in pair) for pair in frequencies)
    if not frequencies or len(frequencies[0]) != 2 or not frequencies[0][0]:
        raise ValueError("nonempty m-by2-by-n low frequency vectors required")
    n, m = len(frequencies[0][0]), len(frequencies)
    if m < n+2 or any(len(pair) != 2 or any(len(row) != n for row in pair) for pair in frequencies):
        raise ValueError("rectangular low source with m>=n+2 required")
    if any(type(a) is not int or a not in (0, 1, 2) for pair in frequencies for row in pair for a in row):
        raise ValueError("canonical low frequencies required")
    anchor = tuple(anchor)
    if len(anchor) != m or any(type(x) is not int or x not in (0, 1, 2) for x in anchor):
        raise ValueError("canonical native anchor word required")
    zero = (0,)*n
    tables = tuple((zero, *pair) for pair in frequencies)
    differences = tuple(tuple((table[(x+1) % 3][l]-table[x][l]) % 3 for l in range(n))
                        for table, x in zip(tables, anchor))
    matrix = nmod_mat([[d[l] for d in differences] for l in range(n)], 3)
    reduced, rank = matrix.rref()
    rows = [tuple(int(reduced[i, j]) for j in range(m)) for i in range(rank)]
    pivots = tuple(next(j for j, a in enumerate(row) if a) for row in rows)
    free = tuple(j for j in range(m) if j not in pivots)
    w = [0]*m
    w[free[0]] = w[free[1]] = 1
    for p, row in zip(pivots, rows):
        w[p] = -(row[free[0]]+row[free[1]]) % 3
    first_one = next(i for i, a in enumerate(w) if a == 1)
    u = tuple(int(a == 2 or (a == 1 and i == first_one)) for i, a in enumerate(w))
    v = tuple(int(a == 2 or (a == 1 and i != first_one)) for i, a in enumerate(w))
    words = (anchor, tuple((x+a) % 3 for x, a in zip(anchor, u)),
             tuple((x+a) % 3 for x, a in zip(anchor, v)))
    assert len(set(words)) == 3 and all(sum(d[l]*a for d, a in zip(differences, w)) % 3 == 0 for l in range(n))
    return {"words": words, "difference_columns": differences, "kernel_word": tuple(w),
            "first_binary_mask": u, "second_binary_mask": v,
            "kernel_pivots": pivots, "kernel_free_coordinates": free,
            "anchor_assignment_enumeration_used": False,
            "coherent_inverse_or_cycle_completion_supplied": False}


def pointed_output(source, anchor):
    record = pointed_words(low_source(source), anchor)
    values = tuple(source.value(word) for word in record["words"])
    q = source.modulus
    assert all(sum(row[l] for row in values) % 3 == 0 for l in range(source.dimension))
    first, second = (tuple((x-y) % q for x, y in zip(values[j], values[0])) for j in (1, 2))
    labels = tuple(inverse_frequency_coordinates(a, b, source.level-1) for a, b in zip(first, second))
    return {**record, "even_parent_level": source.level, "odd_output_level": source.level-1,
            "phase_modulus": q, "relative_first": first, "relative_second": second,
            "native_odd_output_labels": labels, "phase_modulus_not_divided_or_replaced_by_field": True,
            "some_full_parent_order_relative_phase": math.gcd(q, *first, *second) == 1,
            "single_triple_projector_acceptance": str(Fraction(3, 3**source.inputs)),
            "expected_input_qutrits_for_this_independent_projector": str(Fraction(source.inputs*3**source.inputs, 3)),
            "pointed_witness_is_a_quantum_receiver": False}


def pointed_source_ledger(n):
    _integer(n, "source dimension")
    m = n+2
    binary_pairs = (2**m-1)*(2**m-2)
    b = min(Fraction(1), Fraction(binary_pairs, 3**(2*n)))
    e = Fraction(1, 3**n)
    return {"dimension": n, "even_native_input_width": m,
            "ordered_nonzero_distinct_binary_masks": str(binary_pairs),
            "uniform_anchor_zero_low_output_probability_upper": str(b),
            "uniform_anchor_native_odd_TV_upper": str(max(b, e)),
            "two_high_output_vectors_uniform_conditionally_on_low_labels_and_anchor": True,
            "conditional_high_source_proof": "two mask columns(1,0),(0,1) have an integer unit minor; each local high difference is uniform",
            "nonzero_low_output_law": "uniform on F3^n minus0 by GL_n(F3) equivariance",
            "full_parent_order_iff_low_output_nonzero": True,
            "uniform_independent_classical_anchor_required": True,
            "weighted_cover_native_TV_transfer_proved_without_acceptance_lower_bound": False,
            "weighted_cover_zero_low_unconditional_mass_upper": str(min(Fraction(1), 3*b)),
            "coherent_pointed_cover_compiler_supplied": False,
            "new_full_depth_algorithm": False}


def incoming_cases(frequencies, vertex, corner):
    """Polynomial case reduction of FULL-RANK endpoint inversion.

    Corner1 leaves a three-choice low-modulus witness problem. Corner2 is
    linear in its unknown kernel coefficients, with domain restrictions.
    This creates equations, not an incoming-neighbor oracle.
    """
    sample = pointed_words(frequencies, vertex)
    m, n = len(vertex), len(frequencies[0][0])
    if m != n+2 or type(corner) is not int or corner not in (1, 2):
        raise ValueError("endpoint corner1/2 and m=n+2 required")
    vertex = sample["words"][0]
    zero = (0,)*n
    tables = [(zero, *pair) for pair in frequencies]
    current = [tuple((t[(j+1) % 3][l]-t[j][l]) % 3 for l in range(n)) for t, j in zip(tables, vertex)]
    previous = [tuple((t[j][l]-t[(j-1) % 3][l]) % 3 for l in range(n)) for t, j in zip(tables, vertex)]
    cases = []
    for free in combinations(range(m), 2):
        pivots = tuple(j for j in range(m) if j not in free)
        for first_one in (*[j for j in pivots if j < free[0]], free[0]):
            variables = tuple(j for j in pivots if j != first_one)
            fixed = []
            for f in free:
                if corner == 1:
                    fixed.append(previous[f] if f == first_one else current[f])
                else:
                    fixed.append(current[f] if f == first_one else previous[f])
            if first_one in pivots:
                fixed.append(previous[first_one] if corner == 1 else current[first_one])
            target = tuple(-sum(row[l] for row in fixed) % 3 for l in range(n))
            choices = [(zero, current[j] if corner == 1 else previous[j], tuple(-a % 3 for a in previous[j])) for j in variables]
            domains = tuple((0, 2) if j < first_one else (0, 1, 2) for j in variables)
            cases.append({"corner": corner, "free": free, "pivots": pivots, "first_one": first_one,
                          "variables": variables, "coefficient_domains": domains,
                          "choice_vectors": choices, "target": target,
                          "equations_linear_in_coefficients": corner == 2,
                          "incoming_enumeration_oracle_supplied": False})
    return cases


def verify_incoming_case(frequencies, vertex, case, coefficients):
    coefficients = tuple(coefficients)
    if len(coefficients) != len(case["variables"]) or any(type(x) is not int or x not in domain for x, domain in zip(coefficients, case["coefficient_domains"])):
        raise ValueError("one legal coefficient per inverse-case variable required")
    value = tuple(sum(choices[c][l] for choices, c in zip(case["choice_vectors"], coefficients)) % 3 for l in range(len(case["target"])))
    if value != tuple(case["target"]):
        return None
    w = [0]*len(vertex)
    for f in case["free"]:
        w[f] = 1
    w[case["first_one"]] = 1
    for j, c in zip(case["variables"], coefficients):
        w[j] = c
    p, corner = case["first_one"], case["corner"]
    step = tuple(int(a == 2 or (a == 1 and (j == p if corner == 1 else j != p))) for j, a in enumerate(w))
    anchor = tuple((a-b) % 3 for a, b in zip(vertex, step))
    generated = pointed_words(frequencies, anchor)
    if (tuple(generated["kernel_free_coordinates"]) != tuple(case["free"])
            or tuple(generated["kernel_pivots"]) != tuple(case["pivots"])
            or generated["kernel_word"] != tuple(w) or generated["words"][corner] != tuple(vertex)):
        return None
    return anchor


def inverse_geometry_ledger(n):
    _integer(n, "dimension")
    m = n+2
    C = m*math.comb(m, 2)  # Conservative cases per endpoint, no assignment listing.
    moment = (1+2*C)*(1+4*C)
    full_rank_mass = Fraction(17, 18)
    cap = math.ceil(2*moment/full_rank_mass)
    acceptance = 3*full_rank_mass/(2*cap)
    base = pointed_source_ledger(n)
    return {"dimension": n, "physical_width": m,
            "full_rank_inverse_cases_per_endpoint_upper": C,
            "each_unfiltered_case_solution_second_moment_upper": 2,
            "full_rank_anchored_incidence_degree_second_moment_upper": str(moment),
            "native_average_full_rank_anchor_mass_lower": str(full_rank_mass),
            "native_average_retained_anchor_fraction_lower": str(full_rank_mass/2),
            "theoretical_degree_truncation_cap": str(cap),
            "native_average_truncated_cover_acceptance_lower": str(acceptance),
            "accepted_odd_native_TV_upper_if_this_cover_is_compiled": str(min(Fraction(1), max(Fraction(base["uniform_anchor_zero_low_output_probability_upper"])*2/full_rank_mass, Fraction(1, 3**n)))),
            "requires_complete_coherent_incoming_enumerator": True,
            "incoming_corner2_cases_linear": True,
            "incoming_corner1_cases_three_choice_modular_witness": True,
            "full_rank_filter_and_degree_truncation_failures_charged": True,
            "geometry_bound_is_efficient_quantum_compiler": False,
            "one_output_per_n_plus2_stage_closes_full_recursion": False,
            "status": "LOCAL_SOURCE_GEOMETRY_DERIVATION_REVIEW_PENDING"}


def random_native_source(n, level, seed):
    _integer(n, "dimension")
    _integer(level, "even native level", 2)
    if level % 2:
        raise ValueError("even native source required")
    rng = random.Random(seed)
    h0, _, h1 = ideal_chart(level)[0]
    return native_source([[(rng.randrange(h0), rng.randrange(h1)) for _ in range(n)] for _ in range(n+2)], level)


def _weights_and_dual(edges, D):
    row, column = zip(*((v, j) for j, edge in enumerate(edges) for v in edge))
    incidence = coo_matrix((np.ones(len(row)), (row, column)), shape=(D, len(edges))).tocsc()
    solution = linprog(-np.ones(len(edges)), A_ub=incidence, b_ub=np.ones(D), bounds=(0, None), method="highs")
    if not solution.success:
        raise ArithmeticError("bounded cover LP failed")
    # Floating optimization proposes a certificate; exact rational checks and
    # conservative rescaling, not solver status, establish its inequalities.
    weights = [Fraction(max(0., float(x))).limit_denominator(1000000) for x in solution.x]
    loads = [sum((weights[j] for j, e in enumerate(edges) if v in e), Fraction(0)) for v in range(D)]
    scale = max(Fraction(1), max(loads))
    weights = [x/scale for x in weights]
    prices = [Fraction(max(0., -float(x))).limit_denominator(1000000) for x in solution.ineqlin.marginals]
    minimum = min(sum((prices[v] for v in e), Fraction(0)) for e in edges)
    if not minimum:
        raise ArithmeticError("rationalized cover dual has zero edge price")
    prices = [x/min(Fraction(1), minimum) for x in prices]
    assert all(sum((weights[j] for j, e in enumerate(edges) if v in e), Fraction(0)) <= 1 for v in range(D))
    assert all(sum((prices[v] for v in e), Fraction(0)) >= 1 for e in edges)
    return weights, prices


def cover_control(source, *, optimize=True):
    if source.inputs > 8:
        raise ValueError("explicit cover enumeration is calibration only, m<=8")
    points = tuple(product(range(3), repeat=source.inputs))
    index = {word: j for j, word in enumerate(points)}
    low = low_source(source)
    pointed = [pointed_words(low, x) for x in points]
    oriented = [tuple(index[v] for v in record["words"]) for record in pointed]
    edges = tuple(sorted(set(tuple(sorted(e)) for e in oriented)))
    degrees = Counter(v for edge in edges for v in edge)
    endpoint_counts = Counter(e[1] for e in oriented)
    seen, collision = {}, None
    for j, edge in enumerate(oriented):
        if edge[1] in seen:
            collision = (seen[edge[1]], j, edge[1])
            break
        seen[edge[1]] = j
    closed = sum(set(oriented[v]) == set(edge) for edge in oriented for v in edge)
    out = {"dimension": source.dimension, "native_level": source.level, "native_labels": source.labels,
           "input_qutrits": source.inputs, "physical_words_enumerated": len(points),
           "low_only_pointed_finder_calls": len(points), "distinct_three_word_edges": len(edges),
           "maximum_incidence_degree": max(degrees.values()),
           "endpoint_forward_map_is_bijective": len(endpoint_counts) == len(points),
           "endpoint_collision_anchor_ids": collision,
           "pointed_oriented_edges": oriented,
           "incident_oriented_edges_with_same_unordered_pointer": closed,
           "total_pointed_incidence_checks": 3*len(points),
           "uniform_edge_weight_acceptance": str(Fraction(3*len(edges), len(points)*max(degrees.values()))),
           "uniform_scalable_cover_compiler_supplied": False,
           "full_cube_table_and_incidence_index_free": False,
           "all_word_assignments_explicitly_enumerated": True,
           "unknown_preparation_or_inverse_used": False,
           "speedup_claim_allowed": False}
    if not optimize:
        return out
    weights, prices = _weights_and_dual(edges, len(points))
    D = len(points)
    lower = 3*sum(weights, Fraction(0))/D
    upper = min(Fraction(1), 3*sum(prices, Fraction(0))/D)
    assert lower <= upper
    loads = [sum((weights[j] for j, e in enumerate(edges) if v in e), Fraction(0)) for v in range(D)]
    secret = tuple((source.modulus-1-l) % source.modulus for l in range(source.dimension))
    phase = np.array([sum(s*f for s, f in zip(secret, source.value(word))) % source.modulus for word in points])
    state = np.exp(2j*np.pi*phase/source.modulus)/np.sqrt(D)
    edge_records, amplitude_error, measured_mass = [], 0., 0.
    for edge, weight in zip(edges, weights):
        vertices = tuple(points[v] for v in edge)
        values = [source.value(word) for word in vertices]
        first, second = (tuple((a-b) % source.modulus for a, b in zip(values[j], values[0])) for j in (1, 2))
        labels = tuple(inverse_frequency_coordinates(a, b, source.level-1) for a, b in zip(first, second))
        branch = np.sqrt(float(weight))*state[list(edge)]
        mass = float(sum(abs(branch)**2))
        measured_mass += mass
        if weight:
            expected = np.exp(2j*np.pi*np.array([sum(s*f for s, f in zip(secret, value)) % source.modulus for value in values])/source.modulus)/np.sqrt(3)
            amplitude_error = max(amplitude_error, float(max(abs(branch/np.sqrt(mass)-expected))))
        edge_records.append({"vertex_ids": edge, "Kraus_weight": str(weight),
                             "relative_first": first, "relative_second": second,
                             "native_odd_output_labels": labels})
    rejection_mass = float(sum((1-float(load))*abs(a)**2 for load, a in zip(loads, state)))
    assert abs(measured_mass-float(lower)) < 1e-12 and abs(measured_mass+rejection_mass-1) < 1e-12 and amplitude_error < 1e-12
    return {**out, "edge_records": edge_records, "dual_vertex_prices": [str(x) for x in prices],
            "exact_implemented_acceptance": str(lower), "exact_cover_acceptance_upper": str(upper),
            "exact_failure_mass": str(1-lower), "rational_primal_and_dual_verified": True,
            "calibration_secret": secret, "maximum_branch_amplitude_error": amplitude_error,
            "complete_Kraus_probability_error": abs(measured_mass+rejection_mass-1),
            "all_accepted_outputs_evaluated_at_parent_phase_modulus": True,
            "accepted_native_IID_low_source_transfer_proved": False,
            "explicit_compiled_incidence_entries": 3*len(edges)+D,
            "table_compilation_polynomial_in_3_to_m_not_in_m": True}


def run_controls():
    controls = [cover_control(random_native_source(n, 4, 64100+n), optimize=n <= 3) for n in range(1, 7)]
    pointed = []
    for n, level in ((2, 4), (4, 8), (8, 16)):
        source = random_native_source(n, level, 64300+n+level)
        record = pointed_output(source, tuple(j % 3 for j in range(source.inputs)))
        pointed.append({"native_labels": source.labels, **record,
                        "classical_arithmetic_cost_scope": "GF3 elimination plus O(n*m) known modular arithmetic; bit length charged"})
    return {"status": "CONSTRUCTIVE_POINTED_NATIVE_SOURCE_OPEN_COHERENT_COVER_REVIEW_PENDING",
            "growing_root_pointed_outputs": pointed, "explicit_cover_controls": controls,
            "uniform_anchor_source_ledgers": [pointed_source_ledger(n) for n in (8, 16, 32, 64, 128)],
            "conditional_inverse_geometry_ledgers": [inverse_geometry_ledger(n) for n in (8, 16, 32, 64, 128)],
            "claim_gate": {"candidate_accepted": False, "efficient_coherent_extractor": False,
                           "new_full_depth_algorithm": False, "generic_nonlinear_receiver_no_go": False},
            "next_task": "Compile a low-defined efficiently indexable nonlinear cover or group action, with source-weight and recursion costs; pointed forward maps are not permutations."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "pointed_full_root_controls": 3,
                      "efficient_coherent_extractor": False}))


if __name__ == "__main__":
    main()
