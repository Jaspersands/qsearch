"""Costed nonlinear phase descent and native fibre existence/noise frontiers.

LOCAL DERIVATION / REVIEW PENDING. The reference matcher is exponential.
Neither even fibre cardinality nor worst-case counting hardness settles the
complexity of a native-average coherent pairing program.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
from random import Random

import networkx as nx

from dcp_pairing_programs import noise_mass_envelope
from theorems.dcp_adaptive_direction_rank_gate import dyadic, integer
from theorems.dcp_adaptive_affine_packet_receiver import REPORT as AFFINE_REPORT, exact_json


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_nonlinear_fiber_pairing.json"
CONTRACT = ROOT / "research/hypotheses/dcp_nonlinear_fiber_pairing_contract.json"


def instance(labels, phase_bits, descent_bits, max_width=12):
    integer(phase_bits, "phase bits", 3, 4096)
    integer(descent_bits, "descent bits", 1, phase_bits - 1)
    labels = tuple(tuple(row) for row in labels)
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular public labels required")
    if len(labels[0]) > max_width or len(labels) * len(labels[0]) > 4096:
        raise ValueError("UNKNOWN: complete finite source-reference cap")
    for row in labels:
        for a in row:
            integer(a, "canonical full public label", 0, (1 << phase_bits) - 1)
    return labels


def phase_value(labels, x, modulus):
    return tuple(sum(a * ((x >> i) & 1) for i, a in enumerate(row)) % modulus for row in labels)


def useful_relation(labels, phase_bits, descent_bits, x, y):
    q, K = 1 << phase_bits, 1 << descent_bits
    a, b = phase_value(labels, x, q), phase_value(labels, y, q)
    return a != b and all((v - u) % K == 0 for u, v in zip(a, b))


def native_bound(n, phase_bits, descent_bits, copies):
    for v, name in ((n, "components"), (copies, "original copies")):
        integer(v, name, 1, 1000000)
    integer(phase_bits, "phase bits", 3, 4096)
    integer(descent_bits, "descent bits", 1, phase_bits - 1)
    if max(copies, n * phase_bits, n * descent_bits) > 2000000:
        raise ValueError("UNKNOWN: exact probability ledger cap")
    K = 1 << descent_bits
    parity_forced = copies > n * (K - 1)
    odd_failure = Fraction(0) if parity_forced else min(Fraction(1), Fraction(1 << (n * descent_bits), 1 << copies))
    fine_failure = Fraction((1 << copies) - 1, 1 << (n * phase_bits))
    collision_lower = max(Fraction(0), 1 - odd_failure - fine_failure)
    # A maximal COARSE-only pairing is independent of every higher label.
    # Each paired signed sum is therefore uniform modulo q/K, not merely
    # different from other full fibre values with high probability.
    nonzero = 1 - Fraction(1, 1 << (n*(phase_bits-descent_bits)))
    lower = (1 - odd_failure) * nonzero
    if lower < collision_lower:
        raise ArithmeticError("coarse source-law bound should dominate the collision deletion bound")
    return {
        "secret_vector_components": n, "phase_bits": phase_bits,
        "descent_bits": descent_bits, "original_copies": copies,
        "group_algebra_maximum_nonzero_augmentation_degree": n * (K - 1),
        "every_coarse_fibre_even_for_every_A": parity_forced,
        "odd_coarse_fibre_fraction_upper_bound": dyadic(odd_failure),
        "native_mean_fine_collision_endpoint_fraction_upper_bound_uncapped": dyadic(fine_failure),
        "native_mean_optimal_useful_pairing_coverage_lower_bound": dyadic(lower),
        "independent_fine_collision_deletion_lower_bound": dyadic(collision_lower),
        "coarse_only_maximal_pairing_exact_mean_IF_even_fibres": dyadic(nonzero) if parity_forced else None,
        "coarse_only_uniform_higher_label_source_law_used": True,
        "coverage_bound_vacuous": lower == 0,
        "bound_is_for_unconditional_IID_public_A_mean": True,
        "efficient_pairing_program_constructed_by_bound": False,
        "naive_reference_table_rows": {"power_of_two": copies},
        "naive_reference_lookup_comparisons_per_accepted_attempt": {"coefficient": 6, "power_of_two": copies},
        "reference_table_cost_is_not_a_lower_bound_on_structured_programs": True,
        "optimal_full_label_matching_output_IID_proved": False,
    }


def noise_frontier(n, phase_bits, descent_bits, copies, visibility):
    if type(visibility) not in (int, Fraction):
        raise ValueError("exact visibility required")
    visibility = Fraction(visibility)
    if not 0 <= visibility <= 1:
        raise ValueError("visibility outside [0,1]")
    dyadic(visibility)
    if copies > 4096:
        raise ValueError("UNKNOWN: width-envelope work cap")
    bound = native_bound(n, phase_bits, descent_bits, copies)
    lower_record = bound["native_mean_optimal_useful_pairing_coverage_lower_bound"]
    lower = Fraction(int(lower_record["numerator_hex"], 16), 1 << lower_record["denominator_binary_exponent"])
    # Reuse the existing exact fractional-knapsack relaxation. Only its source
    # union bound changes: zero modulo 2^h in n components has rate 2^(-h*n).
    envelope = noise_mass_envelope(n * descent_bits, copies, visibility)
    upper = envelope["upper"]
    radius = copies // 32
    short = min(Fraction(1), Fraction(sum(comb(copies,w) for w in range(1,radius+1)), 1 << (n*descent_bits)))
    tail = min(Fraction(1), short + visibility**(radius+1))
    if upper > tail:
        raise ArithmeticError("knapsack bound exceeds a valid short/tail dual bound")
    if visibility**copies * lower > upper:
        raise ArithmeticError("existential matching exceeds the independent source-width upper bound")
    return dict(bound, visibility=dyadic(visibility),
                native_mean_optimal_useful_visibility_lower_bound=dyadic(visibility**copies * lower),
                native_mean_any_pairing_visibility_upper_bound=dyadic(upper),
                width_capacity_saturating_weight=envelope["capacity_saturating_weight"],
                explicit_short_radius=radius,
                short_width_coverage_upper_bound=dyadic(short),
                short_plus_tail_visibility_upper_bound=dyadic(tail),
                envelope_is_achievable_pairing=False,
                noise_promise="independent balanced ORIGINAL-register dephasing",
                general_quantum_receiver_lower_bound=False)


def augmentation_parity_certificate(labels, phase_bits, descent_bits):
    labels = instance(labels, phase_bits, descent_bits)
    n, m, K = len(labels), len(labels[0]), 1 << descent_bits
    if K**n > 4096:
        raise ValueError("UNKNOWN: finite group-algebra control cap")
    polynomial = {(0,) * n}
    work = 0
    for i in range(m):
        a = tuple(row[i] % K for row in labels)
        # In characteristic two, coefficient of Y^e in (1+Y)^a is odd
        # exactly when each binary digit of e is contained in a.
        factor = {e for e in product(*(range(v + 1) for v in a))
                  if all((e_j & a_j) == e_j for e_j, a_j in zip(e, a))}
        factor.symmetric_difference_update({(0,) * n})
        out = set()
        for u in polynomial:
            for v in factor:
                work += 1
                if work > 1000000:
                    raise ValueError("UNKNOWN: finite polynomial multiplication cap")
                exponent = tuple(x + y for x, y in zip(u, v))
                if max(exponent) >= K:
                    continue
                if exponent in out:
                    out.remove(exponent)
                else:
                    out.add(exponent)
        polynomial = out
    coarse = Counter(phase_value(labels, x, K) for x in range(1 << m))
    odd = sorted(k for k, count in coarse.items() if count & 1)
    # Convert sparse Y terms back to X coordinates independently of the
    # subset-sum recurrence; Y=X+1 in characteristic two.
    odd_from_Y = set()
    for exponent in polynomial:
        for monomial in product(*(range(v + 1) for v in exponent)):
            if not all((e & a) == e for e, a in zip(monomial, exponent)):
                continue
            if monomial in odd_from_Y:
                odd_from_Y.remove(monomial)
            else:
                odd_from_Y.add(monomial)
    if sorted(odd_from_Y) != odd:
        raise ArithmeticError("group-algebra polynomial and original subset fibres disagree")
    if m > n * (K - 1) and polynomial:
        raise ArithmeticError("augmentation nilpotency threshold falsified")
    return {"phase_bits": phase_bits, "descent_bits": descent_bits,
            "public_labels_hex": [[hex(a) for a in row] for row in labels],
            "maximum_augmentation_degree": n * (K - 1),
            "copies": m, "all_fibres_even": not odd,
            "nonzero_Y_monomials": [list(e) for e in sorted(polynomial)],
            "odd_coarse_fibres": [list(x) for x in odd],
            "full_coarse_fibre_counts": [{"residue": list(k), "count": v} for k, v in sorted(coarse.items())],
            "polynomial_products_charged": work}


def lookup_program(table, width):
    integer(width, "lookup width", 1, 8)
    if len(table) != 1 << width or any(c is not None and
            (type(c) is not int or not 0 <= c < 1 << width) for c in table):
        raise ValueError("complete valid-or-failure lookup table required")
    return {"kind": "EXPONENTIAL_LOOKUP_REFERENCE", "width": width, "table": list(table),
            "preprocessing_full_assignments": 1 << width,
            "preprocessing_pair_tests_upper_bound": (1 << width) * ((1 << width)-1)//2,
            "table_lookup_is_a_free_coherent_oracle": False,
            "row_address_comparisons_per_XOR_F": 1 << width,
            "uniform_efficient_program_supplied": False}


def reference_program(labels, phase_bits=4, descent_bits=2):
    labels = instance(labels, phase_bits, descent_bits, max_width=8)
    n, m, q, K = len(labels), len(labels[0]), 1 << phase_bits, 1 << descent_bits
    fine = [phase_value(labels, x, q) for x in range(1 << m)]
    groups = {}
    for x, value in enumerate(fine):
        groups.setdefault(tuple(a % K for a in value), []).append(x)
    table = [None] * (1 << m)
    pair_count_bound = 0
    for vertices in groups.values():
        counts = Counter(fine[x] for x in vertices)
        pair_count_bound += min(len(vertices)//2, len(vertices) - max(counts.values()))
        graph = nx.Graph()
        graph.add_nodes_from(vertices)
        graph.add_edges_from((x, y) for x in vertices for y in vertices if x < y and fine[x] != fine[y])
        for x, y in nx.max_weight_matching(graph, maxcardinality=True):
            table[x], table[y] = y, x
    if sum(c is not None for c in table) != 2 * pair_count_bound:
        raise ArithmeticError("reference maximum matching disagrees with multipartite count")
    return lookup_program(table, m)


def coarse_program(labels, phase_bits=4, descent_bits=2):
    """Exponential reference selecting pairs using ONLY coarse public labels."""
    labels = instance(labels, phase_bits, descent_bits, max_width=8)
    m, K = len(labels[0]), 1 << descent_bits
    coarse = tuple(tuple(a % K for a in row) for row in labels)
    groups = {}
    for x in range(1 << m):
        groups.setdefault(phase_value(coarse, x, K), []).append(x)
    table = [None]*(1 << m)
    for vertices in groups.values():
        for x, y in zip(vertices[::2], vertices[1::2]):
            table[x], table[y] = y, x
    program = lookup_program(table, m)
    program.update(selection_access="coarse-public-labels-only",
                   selection_does_not_read_higher_bits_by_this_construction=True)
    return program


def higher_label_source_control(coarse, phase_bits, descent_bits):
    """Exhaust ALL higher lifts, fixing the actual coarse-only program first."""
    coarse = instance(coarse, phase_bits, descent_bits, max_width=6)
    n, m, K = len(coarse), len(coarse[0]), 1 << descent_bits
    R = 1 << (phase_bits-descent_bits)
    if any(a >= K for row in coarse for a in row) or R**(n*m) > 4096:
        raise ValueError("UNKNOWN: complete high-label lineage control cap")
    program = coarse_program(coarse, phase_bits, descent_bits)
    pairs = [(x,y) for x,y in enumerate(program["table"]) if y is not None and x < y]
    if not pairs:
        raise ValueError("nonempty coarse admission required")
    histograms = [Counter() for _ in pairs]
    for lift in product(range(R), repeat=n*m):
        A = tuple(tuple(coarse[j][i]+K*lift[j*m+i] for i in range(m)) for j in range(n))
        for index, (x,y) in enumerate(pairs):
            delta = tuple(sum(a*(((y>>i)&1)-((x>>i)&1)) for i,a in enumerate(row)) for row in A)
            if any(d % K for d in delta):
                raise ArithmeticError("coarse selected pair violates source divisibility")
            histograms[index][tuple(d//K % R for d in delta)] += 1
    if any(len(hist) != R**n or len(set(hist.values())) != 1 for hist in histograms):
        raise ArithmeticError("coarse-only higher-label uniformity falsified")
    return {
        "coarse_labels": coarse, "phase_bits": phase_bits, "descent_bits": descent_bits,
        "program_fixed_before_higher_lifts": program,
        "higher_label_lifts_enumerated": R**(n*m),
        "per_pair_output_histograms": [
            {"endpoints": list(pair), "counts": [{"label": list(k), "count": v} for k,v in sorted(hist.items())]}
            for pair,hist in zip(pairs,histograms)],
        "coarse_admission_probability": dyadic(Fraction(2*len(pairs),1<<m)),
        "joint_coarse_admission_and_nonzero_label_probability": dyadic(Fraction(2*len(pairs),1<<m)*(1-Fraction(1,R**n))),
        "uniform_output_before_zero_filter": True,
        "uniform_nonzero_output_after_charged_zero_filter": True,
        "pure_input_uniform_native_source_restorable_by_public_zero_injection": True,
        "fresh_independent_source_batches_required": True,
        "native_output_interface_discards_original_higher_label_transcript": True,
        "uniformity_is_conditioned_on_old_full_A": False,
        "public_zero_injection_channel_implemented": False,
        "noisy_zero_injection_automatically_matches_exact_visibility": False,
        "full_label_dependent_programs_inherit_this_law": False,
        "efficient_program_supplied": False,
    }


def program_value(program, x):
    m = program["width"]
    integer(m, "program width", 1, 4096)
    integer(x, "program input", 0, (1 << m) - 1)
    if program["kind"] == "PUBLIC_SINGLE_FLIP":
        mask = program["mask"]
        integer(mask, "flip mask", 1, (1 << m)-1)
        if mask & (mask - 1):
            raise ValueError("single ORIGINAL physical flip required")
        return x ^ mask
    if program["kind"] == "POLYNOMIAL_DISJOINT_PARITY_KERNEL":
        from theorems.dcp_disjoint_kernel_pairing import partner
        return partner(program, x)
    if m > 12:
        raise ValueError("UNKNOWN: exponential lookup reference cap")
    if program["kind"] != "EXPONENTIAL_LOOKUP_REFERENCE" or len(program["table"]) != 1 << m:
        raise ValueError("unsupported or incomplete pairing program")
    value = program["table"][x]
    if value is not None:
        integer(value, "proposal image", 0, (1 << m)-1)
    return value


ACCEPT_OPS = ("F_x_u", "F_u_v", "toggle_accept", "F_u_v", "F_x_u")
ORDER_OPS = ("F_x_u", "toggle_orientation", "swap_x_u", "F_x_u")


def wire_map(word, program, labels, phase_bits, descent_bits, stage, inverse=False):
    """Exact basis-wire compiler; every primitive is an involutive full-space gate.

    x[m], u[m+1], v[m+1], accept, orientation. A valid F output is 2^m+F(x).
    This is the existing six-call reciprocal construction with a vector
    divisibility/nonzero predicate, not a new matching principle.
    """
    m = program["width"]
    integer(m, "program width", 1, 4096)
    integer(word, "packed wires", 0, (1 << (3*m+4))-1)
    if len(labels[0]) != m:
        raise ValueError("program width/source mismatch")
    if stage not in ("accept", "order"):
        raise ValueError("unknown compiler stage")
    size, mask = 1 << m, (1 << m)-1
    us, vs, az, ez = m, 2*m+1, 3*m+2, 3*m+3
    ops = ACCEPT_OPS if stage == "accept" else ORDER_OPS
    for op in reversed(ops) if inverse else ops:
        if op.startswith("F_"):
            source_shift, target_shift = (0, us) if op == "F_x_u" else (us, vs)
            image = program_value(program, (word >> source_shift) & mask)
            word ^= (0 if image is None else size + image) << target_shift
        elif op == "toggle_accept":
            x, u, v = word & mask, (word >> us) & (2*size-1), (word >> vs) & (2*size-1)
            valid = (u >= size and v >= size and (v & mask) == x
                     and useful_relation(labels, phase_bits, descent_bits, x, u & mask))
            word ^= int(valid) << az
        elif op == "toggle_orientation":
            word ^= int((word & mask) > ((word >> us) & mask)) << ez
        else:
            swap = ((word >> ez) & 1) * ((word & mask) ^ ((word >> us) & mask))
            word ^= swap ^ (swap << us)
    return word


def compiler_certificate(labels, phase_bits, descent_bits, program):
    labels = instance(labels, phase_bits, descent_bits)
    m, q, K = len(labels[0]), 1 << phase_bits, 1 << descent_bits
    if program.get("table_lookup_is_a_free_coherent_oracle") is not False:
        raise ValueError("free coherent lookup assumption rejected")
    if program["kind"] == "EXPONENTIAL_LOOKUP_REFERENCE" and (
            program.get("row_address_comparisons_per_XOR_F") != 1 << m
            or program.get("uniform_efficient_program_supplied") is not False):
        raise ValueError("exponential program cost cannot be waived")
    pairs, accepted = [], []
    for x in range(1 << m):
        w = wire_map(x, program, labels, phase_bits, descent_bits, "accept")
        valid = bool(w >> (3*m+2) & 1)
        expected = x | (int(valid) << (3*m+2))
        if w != expected:
            raise ArithmeticError("acceptance work not clean")
        if not valid:
            continue
        accepted.append(x)
        output = wire_map(w, program, labels, phase_bits, descent_bits, "order")
        r, e = output & ((1 << m)-1), output >> (3*m+3) & 1
        if output != r | (1 << (3*m+2)) | (e << (3*m+3)):
            raise ArithmeticError("endpoint ordering work not clean")
        c = program_value(program, r)
        if {r, c} != {x, program_value(program, x)} or r >= c:
            raise ArithmeticError("unordered reciprocal pair")
        if not e:
            first, second = phase_value(labels, r, q), phase_value(labels, c, q)
            label = tuple(((b-a) % q)//K for a, b in zip(first, second))
            if not any(label):
                raise ArithmeticError("zero descended label received credit")
            pairs.append({"first": r, "second": c, "descended_label_hex": [hex(v) for v in label],
                          "physical_Hamming_width": (r ^ c).bit_count(),
                          "unconditional_pair_probability": dyadic(Fraction(2, 1 << m))})
    return {"phase_bits": phase_bits, "descent_bits": descent_bits,
            "public_labels_hex": [[hex(a) for a in row] for row in labels],
            "program": program, "pairs": pairs,
            "accepted_assignments": accepted,
            "useful_descent_probability": dyadic(Fraction(len(accepted), 1 << m)),
            "accepted_XOR_F_calls": 6, "failed_XOR_F_calls": 4,
            "original_unknown_phase_qubits_per_attempt": m,
            "compiler_qubits_excluding_F_internal_work": 3*m+4,
            "output_qubits_on_accepted_attempt": 1,
            "pair_list_is_measurement_outcomes_not_parallel_outputs": True,
            "known_public_relation_bit_arithmetic_order": "O(n*m*t) per check plus reversible cleanup",
            "basis_wire_permutations_and_clean_accepted_workspace_implemented": True,
            "hardware_gate_export_backend_implemented": False,
            "secret_or_phase_evaluator_is_program_input": False,
            "fresh_descended_labels_IID_certified": False,
            "same_A_source_resupply_or_inverse_supplied": False}


def exact_one_encoding(clauses, variables):
    """Polynomial-size counting reduction with a simple pairing counterexample.

    No SAT/fibre enumeration. Repeated variable occurrences are represented
    by integer multiplicities, not silently deduplicated.
    """
    integer(variables, "Boolean variables", 1, 4096)
    clauses = tuple(tuple(c) for c in clauses)
    if not clauses:
        raise ValueError("nonempty exact-one constraint system required")
    for clause in clauses:
        if len(clause) != 3 or any(type(i) is not int or not 0 <= i < variables for i in clause):
            raise ValueError("three indexed Boolean occurrences per exact-one constraint")
    n, padding = len(clauses), max(1, 3*len(clauses)+1-variables)
    if variables + padding > 4096 or n*(variables+padding) > 2000000:
        raise ValueError("UNKNOWN: polynomial encoding matrix cap")
    rows = [[0]*(variables+padding) for _ in range(n)]
    for j, clause in enumerate(clauses):
        for i in clause:
            rows[j][i] += 1
    rows[0][variables] = 4  # Coarse-zero, full-nonzero public padding coordinate.
    rows = tuple(tuple(row) for row in rows)
    program = {"kind": "PUBLIC_SINGLE_FLIP", "width": variables+padding,
               "mask": 1 << variables, "uniform_efficient_program_supplied": True,
               "CNOT_gates_per_XOR_F": variables+padding,
               "X_gates_per_XOR_F": 2,
               "table_lookup_is_a_free_coherent_oracle": False}
    return {"clauses": clauses, "original_variables": variables, "padding_variables": padding,
            "labels": rows, "program": program}


def exact_one_counting_reduction(clauses, variables):
    encoding = exact_one_encoding(clauses, variables)
    clauses, rows = encoding["clauses"], encoding["labels"]
    n, padding = len(clauses), encoding["padding_variables"]
    if variables + padding > 10:
        raise ValueError("UNKNOWN: finite reduction-control enumeration cap")
    direct = sum(all(sum((x >> i) & 1 for i in clause) == 1 for clause in clauses)
                 for x in range(1 << variables))
    count = sum(phase_value(rows, x, 4) == (1,)*n for x in range(1 << (variables+padding)))
    if count != direct * (1 << padding):
        raise ArithmeticError("exact-one/fibre count with known padding multiplier failed")
    return {"clauses": clauses, "original_variables": variables, "padding_variables": padding,
            "public_labels_hex": [[hex(a) for a in row] for row in rows],
            "exact_one_satisfying_assignments": direct, "coarse_target": [1]*n,
            "coarse_target_fibre_count": count, "known_count_multiplier": 1 << padding,
            "simple_useful_pairing": compiler_certificate(rows, 3, 2, encoding["program"]),
            "counting_hardness_implies_general_pairing_hardness": False,
            "native_IID_average_case_hardness_reduction_supplied": False,
            "pairing_solves_exact_one_counting": False,
            "this_countercontrol_is_a_candidate_algorithm": False}


def build_report():
    source_raw = AFFINE_REPORT.read_bytes()
    source = json.loads(source_raw)
    controls = []
    for key, case in (("unfiltered-seed-2", source["source_controls"][2]),
                      ("unfiltered-seed-5", source["source_controls"][5]),
                      ("SELECTED-grammar-gap-94", source["affine_grammar_gap_counterexample"])):
        labels = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
        record = compiler_certificate(labels, 4, 2, reference_program(labels))
        record.update(source_control=key,
                      source_affine_useful_descent_probability=case["optimal_feedback_useful_descent_probability"],
                      source_arbitrary_pairing_upper_bound=case["arbitrary_basis_pairing_useful_descent_upper_bound"])
        controls.append(record)
    parity = []
    for n, extra in ((1, False), (1, True), (2, False), (2, True)):
        columns = [tuple(int(j == i) for j in range(n)) for i in range(n) for _ in range(3)]
        if extra:
            columns.append(tuple((j+1) % 4 for j in range(n)))
        A = tuple(tuple(column[j] for column in columns) for j in range(n))
        parity.append(augmentation_parity_certificate(A, 4, 2))
    rng = Random(101506)
    parity.append(augmentation_parity_certificate(tuple(tuple(rng.randrange(16) for _ in range(10)) for _ in range(3)), 4, 2))
    growth = [noise_frontier(n, 64, 2, 3*n, v)
              for n in (32,64,128,256,512) for v in (Fraction(1,4),Fraction(3,4),Fraction(63,64))]
    contract = json.loads(CONTRACT.read_text())
    return exact_json({
        "status": "NATIVE_FIBRE_EXISTENCE_NOISE_FRONTIER_AND_EXPONENTIAL_COMPILER_REFERENCE",
        "contract_id": contract["contract_id"],
        "source_affine_artifact": str(AFFINE_REPORT.relative_to(ROOT)),
        "source_affine_sha256": hashlib.sha256(source_raw).hexdigest(),
        "nonlinear_reference_controls": controls, "augmentation_parity_controls": parity,
        "coarse_only_higher_label_source_controls": [
            higher_label_source_control(((1,1,1,1),),4,2),
            higher_label_source_control(((1,1,0),(0,1,1)),3,1)],
        "native_growing_parameter_frontiers": growth,
        "joint_growing_parameter_frontiers": [noise_frontier(n,n,2,3*n,Fraction(n-1,n))
                                               for n in (32,64,128,256,512)],
        "one_extra_copy_parity_frontiers": [native_bound(n,64,2,3*n+1) for n in (32,64,128,256,512)],
        "many_level_existence_only": [native_bound(n,64,62,63*n) for n in (32,64,128)],
        "counting_route_falsifiers": [exact_one_counting_reduction(((0,1,2),(1,2,3)),4),
                                      exact_one_counting_reduction(((0,0,1),),2)],
        "scope": contract["scope"], "remaining_proof_obligations": contract["remaining_proof_obligations"],
        "accepted_speedup_candidate": False, "efficient_native_receiver_supplied": False,
        "external_theorem_review_complete": False,
        "source_quantum_preparations_executed": 0, "novelty_claim": False,
        "existing_six_call_compiler_context": "research/DCP_PAIRING_PROGRAMS.md",
        "existing_width_noise_envelope_reused": "core/dcp_pairing_programs.py:noise_mass_envelope",
    })


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "nonlinear_controls": len(report["nonlinear_reference_controls"]),
                      "native_frontiers": len(report["native_growing_parameter_frontiers"])
                                          +len(report["joint_growing_parameter_frontiers"]),
                      "efficient_native_receiver_supplied": False, "accepted_speedup_candidate": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
