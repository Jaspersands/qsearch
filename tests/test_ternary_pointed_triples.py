from collections import Counter
from fractions import Fraction
from itertools import product
import math

import numpy as np
import pytest

from cyclotomic_fiber_receiver import frequency_coordinates, inverse_frequency_coordinates, native_source
from ternary_pointed_triples import (
    cover_control, incoming_cases, inverse_geometry_ledger, low_source,
    pointed_output, pointed_source_ledger, pointed_words, random_native_source,
    verify_incoming_case,
)


def test_every_point_of_every_small_unfiltered_native_source_has_distinct_valid_triple():
    labels = tuple(product(range(3), repeat=2))
    frequencies = {y: frequency_coordinates(y, 2) for y in labels}
    count, full_rank_edges, degree_square_total = 0, 0, 0
    for ys in product(labels, repeat=3):
        low = tuple(((frequencies[y][0],), (frequencies[y][1],)) for y in ys)
        degrees = Counter()
        for anchor in product(range(3), repeat=3):
            record = pointed_words(low, anchor)
            assert record["words"][0] == anchor and len(set(record["words"])) == 3
            values = [sum((0, *frequencies[y])[j] for y, j in zip(ys, word)) % 3 for word in record["words"]]
            assert sum(values) % 3 == 0
            assert sum(a == 1 for a in record["kernel_word"]) >= 2
            assert not record["anchor_assignment_enumeration_used"]
            if len(record["kernel_pivots"]) == 1:
                full_rank_edges += 1
                degrees.update(record["words"])
            count += 1
        degree_square_total += sum(d*d for d in degrees.values())
    assert count == 19683
    assert Fraction(full_rank_edges, count) == Fraction(26, 27)
    assert Fraction(full_rank_edges, count) >= Fraction(17, 18)
    ledger = inverse_geometry_ledger(1)
    assert Fraction(degree_square_total, count) <= int(ledger["full_rank_anchored_incidence_degree_second_moment_upper"])
    cap = int(ledger["theoretical_degree_truncation_cap"])
    assert Fraction(3*full_rank_edges, cap*count) >= Fraction(ledger["native_average_truncated_cover_acceptance_lower"])


@pytest.mark.parametrize("level", [4, 8, 16])
def test_growing_root_output_is_native_odd_at_the_actual_parent_modulus(level):
    source = random_native_source(4, level, 65200+level)
    record = pointed_output(source, (0, 1, 2, 0, 1, 2))
    assert record["phase_modulus"] == source.modulus
    assert record["phase_modulus_not_divided_or_replaced_by_field"]
    for label, a, c in zip(record["native_odd_output_labels"], record["relative_first"], record["relative_second"]):
        assert frequency_coordinates(label, level-1) == (a, c)
        assert c % 3 == 2*a % 3
    assert Fraction(record["single_triple_projector_acceptance"]) == Fraction(3, 3**source.inputs)
    assert not record["pointed_witness_is_a_quantum_receiver"]


@pytest.mark.parametrize("anchor", [(0, 0, 0), (1, 2, 0)])
def test_all_actual_native_high_lifts_produce_uniform_high_output_pair(anchor):
    original = random_native_source(1, 4, 65210)
    lows = [tuple(v[0] % 3 for v in pair) for pair in original.frequencies]
    counts = Counter()
    for lifts in product(range(3), repeat=6):
        labels = [[inverse_frequency_coordinates(a+3*lifts[2*i], c+3*lifts[2*i+1], 4)] for i, (a, c) in enumerate(lows)]
        source = native_source(labels, 4)
        record = pointed_output(source, anchor)
        counts[record["relative_first"][0], record["relative_second"][0]] += 1
    assert len(counts) == 9 and set(counts.values()) == {81}


@pytest.mark.parametrize("n", [1, 2, 3])
def test_inverse_case_reduction_finds_exactly_all_full_rank_incoming_anchors(n):
    source = random_native_source(n, 4, 65300+n)
    frequencies = low_source(source)
    points = tuple(product(range(3), repeat=source.inputs))
    records = {x: pointed_words(frequencies, x) for x in points}
    for vertex in points[::max(1, len(points)//9)]:
        for corner in (1, 2):
            expected = {x for x, record in records.items() if len(record["kernel_pivots"]) == n and record["words"][corner] == vertex}
            found = set()
            for case in incoming_cases(frequencies, vertex, corner):
                assert case["equations_linear_in_coefficients"] == (corner == 2)
                for coefficients in product(*case["coefficient_domains"]):
                    anchor = verify_incoming_case(frequencies, vertex, case, coefficients)
                    if anchor is not None:
                        found.add(anchor)
            assert found == expected


def test_exact_native_average_inverse_case_second_moments_have_correct_independence():
    labels = tuple(product(range(3), repeat=2))
    cache = {y: frequency_coordinates(y, 2) for y in labels}
    totals, counts = {}, Counter()
    for ys in product(labels, repeat=3):
        frequencies = tuple(((cache[y][0],), (cache[y][1],)) for y in ys)
        for corner in (1, 2):
            for j, case in enumerate(incoming_cases(frequencies, (0, 0, 0), corner)):
                number = 0
                for coefficients in product(*case["coefficient_domains"]):
                    value = tuple(sum(choices[c][l] for choices, c in zip(case["choice_vectors"], coefficients)) % 3 for l in range(len(case["target"])))
                    number += value == tuple(case["target"])
                key = corner, j
                counts[key] += number*number
                totals[key] = math.prod(map(len, case["coefficient_domains"]))
    for key, total in totals.items():
        assert Fraction(counts[key], 729) == Fraction(total, 3)+Fraction(total*(total-1), 9)
        assert Fraction(counts[key], 729) <= 2


def test_explicit_nonlinear_cover_has_exact_feasible_quantum_weights_not_a_fast_compiler():
    source = random_native_source(2, 4, 65402)
    record = cover_control(source)
    edges = record["edge_records"]
    D = record["physical_words_enumerated"]
    weights = [Fraction(e["Kraus_weight"]) for e in edges]
    prices = [Fraction(x) for x in record["dual_vertex_prices"]]
    assert all(sum(w for e, w in zip(edges, weights) if v in e["vertex_ids"]) <= 1 for v in range(D))
    assert all(sum(prices[v] for v in e["vertex_ids"]) >= 1 for e in edges)
    assert Fraction(record["exact_implemented_acceptance"]) <= Fraction(record["exact_cover_acceptance_upper"])
    assert record["maximum_branch_amplitude_error"] < 1e-12
    assert record["complete_Kraus_probability_error"] < 1e-12
    assert not record["uniform_scalable_cover_compiler_supplied"]
    assert not record["accepted_native_IID_low_source_transfer_proved"]


def test_Naimark_reference_is_norm_preserving_on_arbitrary_input_not_only_phase_states():
    source = random_native_source(1, 4, 65411)
    record = cover_control(source)
    D = record["physical_words_enumerated"]
    V = np.zeros((3*len(record["edge_records"])+D, D), dtype=complex)
    loads = [Fraction(0)]*D
    for j, edge in enumerate(record["edge_records"]):
        w = Fraction(edge["Kraus_weight"])
        for corner, v in enumerate(edge["vertex_ids"]):
            V[3*j+corner, v] = math.sqrt(float(w))
            loads[v] += w
    for v, load in enumerate(loads):
        V[3*len(record["edge_records"])+v, v] = math.sqrt(float(1-load))
    assert np.max(abs(V.conj().T@V-np.eye(D))) < 1e-12
    rng = np.random.default_rng(65412)
    state = rng.normal(size=D)+1j*rng.normal(size=D)
    assert abs(np.linalg.norm(V@state)-np.linalg.norm(state)) < 1e-12


def test_pointed_forward_map_collision_really_blocks_erasing_anchor_by_that_map():
    source = random_native_source(2, 4, 64102)
    record = cover_control(source, optimize=False)
    a, b, target = record["endpoint_collision_anchor_ids"]
    assert a != b
    assert record["pointed_oriented_edges"][a][1] == record["pointed_oriented_edges"][b][1] == target
    assert not record["endpoint_forward_map_is_bijective"]
    assert record["incident_oriented_edges_with_same_unordered_pointer"] < record["total_pointed_incidence_checks"]


def test_source_and_inverse_geometry_ledgers_are_polynomial_and_scoped():
    for n in (8, 32, 128):
        source = pointed_source_ledger(n)
        inverse = inverse_geometry_ledger(n)
        m = n+2
        C = m*math.comb(m, 2)
        moment = (1+2*C)*(1+4*C)
        assert Fraction(source["uniform_anchor_zero_low_output_probability_upper"]) == min(Fraction(1), Fraction((2**m-1)*(2**m-2), 3**(2*n)))
        assert int(inverse["full_rank_anchored_incidence_degree_second_moment_upper"]) == moment
        cap = int(inverse["theoretical_degree_truncation_cap"])
        assert cap >= 2*moment/Fraction(17, 18)
        assert Fraction(inverse["native_average_truncated_cover_acceptance_lower"]) == Fraction(17, 18)*3/(2*cap)
        assert not inverse["geometry_bound_is_efficient_quantum_compiler"]
        assert not inverse["one_output_per_n_plus2_stage_closes_full_recursion"]


def test_phase_modulus_not_divided_does_not_claim_every_output_has_full_phase_order():
    labels = [[inverse_frequency_coordinates(3, 6, 4)] for _ in range(3)]
    source = native_source(labels, 4)
    record = pointed_output(source, (0, 0, 0))
    assert record["phase_modulus_not_divided_or_replaced_by_field"]
    assert not record["some_full_parent_order_relative_phase"]


def test_invalid_source_and_witness_records_are_rejected():
    with pytest.raises(ValueError):
        pointed_words((((1,), (2,)),)*2, (0, 0))
    with pytest.raises(ValueError):
        pointed_words((((True,), (2,)),)*3, (0, 0, 0))
    with pytest.raises(ValueError):
        pointed_words((((1,), (2,)),)*3, (0, 0, True))
    with pytest.raises(ValueError):
        pointed_output(native_source([[(1, 0)]]*3, 3), (0, 0, 0))
    with pytest.raises(ValueError):
        incoming_cases((((1,), (2,)),)*3, (0, 0, 0), True)
    with pytest.raises(ValueError):
        cover_control(random_native_source(7, 4, 1))
